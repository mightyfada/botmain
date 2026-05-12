import os
import asyncio
import logging
import csv
import time
import threading
import json
import zipfile
import shutil
import io
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, JobQueue
)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_USER_IDS = [
    int(x.strip())
    for x in os.environ.get("ADMIN_USER_IDS", "5011045316").split(",")
    if x.strip()
]
API_ID   = os.environ.get("API_ID",   "23269382")
API_HASH = os.environ.get("API_HASH", "fe19c565fb4378bd5128885428ff8e26")

DATA_DIR     = os.environ.get("DATA_DIR", ".")
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")
PHONE_CSV    = os.path.join(DATA_DIR, "phone.csv")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
CONFIG_FILE  = os.path.join(DATA_DIR, "bot_config.json")
LOG_FILE     = os.path.join(DATA_DIR, "bot.log")

BOT_START_TIME = datetime.now()

os.makedirs(SESSIONS_DIR, exist_ok=True)

# ── Default runtime config (editable via /config) ─────────────────────────────
DEFAULT_CONFIG = {
    "default_delay":       2,
    "auto_scan_hour":      8,       # hour (0-23) for daily auto scan
    "auto_scan_enabled":   False,
    "recent_groups":       [],      # last 5 used source/target groups
    "alert_on_error":      True,
    "clone_filter":        "all",   # all | text | media | text+media
}

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
            # merge with defaults so new keys are always present
            return {**DEFAULT_CONFIG, **cfg}
        except Exception:
            pass
    return dict(DEFAULT_CONFIG)

def save_config(cfg: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

# ══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ══════════════════════════════════════════════════════════════════════════════
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE),
    ],
)
logger = logging.getLogger(__name__)

# ── Global stop flag ───────────────────────────────────────────────────────────
_stop_event = threading.Event()

# ── Operation queue ────────────────────────────────────────────────────────────
_op_queue: list[dict] = []          # [{name, func, args}]
_queue_lock = threading.Lock()

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def log_history(action: str, detail: str):
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE) as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append({
        "ts":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "detail": detail,
    })
    history = history[-100:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def read_phones() -> list[str]:
    if not os.path.exists(PHONE_CSV):
        return []
    with open(PHONE_CSV, "r") as f:
        return [row[0].strip() for row in csv.reader(f) if row and row[0].strip()]

def write_phones(phones: list[str]):
    with open(PHONE_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        for p in phones:
            writer.writerow([p])

def parse_phone(raw: str) -> str:
    from telethon import utils as tu
    try:
        return tu.parse_phone(raw)
    except Exception:
        return raw.strip().lstrip("+")

def get_uptime() -> str:
    delta = datetime.now() - BOT_START_TIME
    h, rem = divmod(int(delta.total_seconds()), 3600)
    m, s   = divmod(rem, 60)
    return f"{h}h {m}m {s}s"

def _add_recent_group(group: str):
    cfg = load_config()
    groups = cfg.get("recent_groups", [])
    if group in groups:
        groups.remove(group)
    groups.insert(0, group)
    cfg["recent_groups"] = groups[:5]
    save_config(cfg)

# ── Admin-only decorator ───────────────────────────────────────────────────────
def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id if update.effective_user else None
        if uid not in ADMIN_USER_IDS:
            target = update.message or (update.callback_query and update.callback_query.message)
            if target:
                await target.reply_text("❌ Unauthorized access.")
            return
        return await func(update, context)
    wrapper.__name__ = func.__name__
    return wrapper

# ══════════════════════════════════════════════════════════════════════════════
class TGTXBot:
    def __init__(self, token: str):
        self.token       = token
        self.application = Application.builder().token(token).build()
        self._active_task: threading.Thread | None = None
        self._setup_handlers()
        self._setup_jobs()

    # ──────────────────────────────────────────────────────────────────────
    # HANDLER REGISTRATION
    # ──────────────────────────────────────────────────────────────────────
    def _setup_handlers(self):
        add = self.application.add_handler
        # commands
        add(CommandHandler("start",     self.cmd_start))
        add(CommandHandler("menu",      self.cmd_menu))
        add(CommandHandler("status",    self.cmd_status))
        add(CommandHandler("cancel",    self.cmd_cancel))
        add(CommandHandler("help",      self.cmd_help))
        add(CommandHandler("history",   self.cmd_history))
        add(CommandHandler("accounts",  self.cmd_accounts))
        add(CommandHandler("health",    self.cmd_health))
        add(CommandHandler("backup",    self.cmd_backup))
        add(CommandHandler("ban",       self.cmd_ban_shortcut))
        add(CommandHandler("limits",    self.cmd_limits_shortcut))
        add(CommandHandler("addadmin",  self.cmd_add_admin))
        add(CommandHandler("removeadmin", self.cmd_remove_admin))
        add(CommandHandler("config",    self.cmd_config))
        add(CommandHandler("queue",     self.cmd_queue))
        # callbacks + messages
        add(CallbackQueryHandler(self.button_handler))
        add(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    def _setup_jobs(self):
        """Schedule the daily auto-scan job."""
        cfg = load_config()
        if cfg.get("auto_scan_enabled"):
            hour = cfg.get("auto_scan_hour", 8)
            self.application.job_queue.run_daily(
                self._job_daily_scan,
                time=datetime.strptime(f"{hour:02d}:00", "%H:%M").time(),
                name="daily_scan",
            )

    # ──────────────────────────────────────────────────────────────────────
    # KEYBOARDS
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def _main_kb():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Account Manager", callback_data="account_manager"),
             InlineKeyboardButton("🚀 Group Tools",     callback_data="group_tools")],
            [InlineKeyboardButton("⚙️ System Tools",    callback_data="system_tools"),
             InlineKeyboardButton("📈 Status",          callback_data="status")],
        ])

    @staticmethod
    def _confirm_kb(yes_cb: str, no_cb: str = "back_to_main"):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Yes, proceed", callback_data=yes_cb),
             InlineKeyboardButton("❌ Cancel",       callback_data=no_cb)],
        ])

    # ──────────────────────────────────────────────────────────────────────
    # COMMANDS
    # ──────────────────────────────────────────────────────────────────────
    @admin_only
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        username = update.effective_user.first_name or "Admin"
        phones   = read_phones()
        task_str = "🔄 Running" if (self._active_task and self._active_task.is_alive()) else "✅ Idle"
        text = (
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🚀 *TGTX Bot Controller v4.0*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👋 Welcome, *{username}*!\n\n"
            f"📱 Accounts: `{len(phones)}` | ⚙️ {task_str}\n\n"
            "🎯 *Features:*\n"
            "• Multi-Account Management & Health Check\n"
            "• Session Backup & Restore\n"
            "• Group Cloning with Filter Options\n"
            "• Real-time Message Forwarding\n"
            "• Limit Checker with Auto-Fix\n"
            "• Ban Detection & Cleanup\n"
            "• Operation Queue & Scheduling\n"
            "• Daily Auto-Scan Reports\n"
            "• Config Editor & Multi-Admin\n\n"
            "⚡ *Status:* ACTIVE & READY\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Select an option below:"
        )
        await update.message.reply_text(text, reply_markup=self._main_kb(), parse_mode="Markdown")

    @admin_only
    async def cmd_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        text = (
            "🤖 *TGTX Main Menu*\n\n"
            "📋 *Commands:*\n"
            "/start · /menu · /status · /health\n"
            "/accounts · /history · /backup\n"
            "/ban · /limits · /config · /queue\n"
            "/addadmin · /removeadmin · /cancel\n\n"
            "Select an option below:"
        )
        await update.message.reply_text(text, reply_markup=self._main_kb(), parse_mode="Markdown")

    @admin_only
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        phones  = read_phones()
        sessions = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
        task_str = "🔄 Running" if (self._active_task and self._active_task.is_alive()) else "✅ Idle"
        q_size   = len(_op_queue)
        cfg      = load_config()
        text = (
            "📈 *System Status*\n\n"
            f"🤖 *Bot:* ✅ Online\n"
            f"⏱ *Uptime:* `{get_uptime()}`\n"
            f"📱 *Accounts:* `{len(phones)}`\n"
            f"💾 *Sessions:* `{len(sessions)}`\n"
            f"⚙️ *Active Op:* {task_str}\n"
            f"📋 *Queue:* `{q_size}` pending\n"
            f"🕐 *Daily Scan:* {'✅ ON @ ' + str(cfg['auto_scan_hour']) + ':00' if cfg['auto_scan_enabled'] else '❌ OFF'}\n"
            f"🔽 *Clone Filter:* `{cfg['clone_filter']}`\n\n"
            "All systems operational! 🎉"
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    @admin_only
    async def cmd_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        _stop_event.set()
        with _queue_lock:
            _op_queue.clear()
        await update.message.reply_text(
            "❌ *Cancelled*\n\nRunning operation stopped and queue cleared.\nUse /menu to start fresh.",
            parse_mode="Markdown"
        )
        await asyncio.sleep(0.5)
        _stop_event.clear()

    @admin_only
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = (
            "📚 *TGTX Bot Help*\n\n"
            "🎯 *All Commands:*\n"
            "`/start` — Welcome banner\n"
            "`/menu` — Main menu\n"
            "`/status` — Full system status\n"
            "`/health` — Quick account health dashboard\n"
            "`/accounts` — List all accounts\n"
            "`/history` — Last 20 operations\n"
            "`/backup` — Get session files as zip\n"
            "`/ban` — Shortcut: remove banned accounts\n"
            "`/limits` — Shortcut: check & fix limits\n"
            "`/config` — View/edit runtime config\n"
            "`/queue` — View operation queue\n"
            "`/addadmin <id>` — Grant admin access\n"
            "`/removeadmin <id>` — Revoke admin access\n"
            "`/cancel` — Stop operation & clear queue\n\n"
            "💡 *Tips:*\n"
            "• Every destructive action has a confirm dialog\n"
            "• Long ops run in background with live updates\n"
            "• Operations queue up — no more blocked tasks\n"
            "• Daily auto-scan configurable via /config\n"
            "• Use /backup before deploying to Railway\n"
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    @admin_only
    async def cmd_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not os.path.exists(HISTORY_FILE):
            await update.message.reply_text("📭 No history yet.")
            return
        with open(HISTORY_FILE) as f:
            history = json.load(f)
        if not history:
            await update.message.reply_text("📭 No history yet.")
            return
        lines = ["📋 *Last 20 Operations:*\n"]
        for h in reversed(history[-20:]):
            lines.append(f"• `{h['ts']}` — *{h['action']}*\n  _{h['detail']}_")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

    @admin_only
    async def cmd_accounts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        phones = read_phones()
        if not phones:
            await update.message.reply_text("📭 No accounts yet. Add some via Account Manager.")
            return
        lines = [f"📱 *Accounts ({len(phones)} total):*\n"]
        for i, p in enumerate(phones, 1):
            lines.append(f"`{i}.` {p}")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

    # ── /health — account health dashboard ────────────────────────────────
    @admin_only
    async def cmd_health(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        phones = read_phones()
        if not phones:
            await update.message.reply_text("📭 No accounts to check.")
            return
        msg = await update.message.reply_text(
            f"🏥 *Health Dashboard*\n\nChecking `{len(phones)}` accounts…",
            parse_mode="Markdown"
        )
        chat_id = update.message.chat_id
        bot     = context.bot

        async def send_update(t):
            try:
                await bot.send_message(chat_id, t, parse_mode="Markdown")
            except Exception:
                pass

        loop = asyncio.get_event_loop()
        def task():
            asyncio.run_coroutine_threadsafe(
                self._do_health_check(send_update, phones), loop
            ).result()

        self._active_task = threading.Thread(target=task, daemon=True)
        self._active_task.start()

    async def _do_health_check(self, send_update, phones: list[str]):
        from pyrogram import Client as PyroClient
        from pyrogram.errors import (
            AuthKeyUnregistered, UserDeactivatedBan,
            SessionExpired, SessionRevoked, UserDeactivated
        )
        active  = []
        banned  = []
        limited = []
        errors  = []

        for phone_raw in phones:
            if _stop_event.is_set():
                break
            phone = parse_phone(phone_raw)
            try:
                app = PyroClient(
                    f"{SESSIONS_DIR}/{phone}",
                    api_id=int(API_ID), api_hash=API_HASH, phone_number=phone
                )
                app.start()
                # quick spambot ping
                app.send_message("spambot", "/start")
                time.sleep(1)
                last = next(app.get_chat_history("spambot", limit=1), None)
                txt  = (last.text or "") if last else ""
                app.stop()
                if "no limits" in txt.lower() or "Good news" in txt:
                    active.append(phone)
                elif "limited" in txt.lower() or "actions can trigger" in txt.lower():
                    limited.append(phone)
                else:
                    active.append(phone)
            except (AuthKeyUnregistered, UserDeactivatedBan, SessionExpired, SessionRevoked, UserDeactivated):
                banned.append(phone)
            except Exception as e:
                errors.append(f"{phone}: {str(e)[:40]}")

        lines = [
            "🏥 *Account Health Dashboard*\n",
            f"✅ Active: `{len(active)}`",
            f"⚠️ Limited: `{len(limited)}`",
            f"⛔ Banned: `{len(banned)}`",
            f"❓ Errors: `{len(errors)}`\n",
        ]
        if banned:
            lines.append("*Banned:*\n" + "\n".join(f"  ⛔ `{p}`" for p in banned))
        if limited:
            lines.append("*Limited:*\n" + "\n".join(f"  ⚠️ `{p}`" for p in limited))
        if errors:
            lines.append("*Errors:*\n" + "\n".join(f"  ❓ {e}" for e in errors[:5]))
        lines.append("\nUse /ban to clean banned, /limits to fix limits.")
        log_history("Health Check", f"Active:{len(active)} Limited:{len(limited)} Banned:{len(banned)}")
        await send_update("\n".join(lines))

    # ── /backup — zip sessions and send ───────────────────────────────────
    @admin_only
    async def cmd_backup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        sessions = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
        if not sessions:
            await update.message.reply_text("📭 No session files found to backup.")
            return
        msg = await update.message.reply_text(
            f"📦 Creating backup of `{len(sessions)}` session(s)…", parse_mode="Markdown"
        )
        try:
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for fname in sessions:
                    fpath = os.path.join(SESSIONS_DIR, fname)
                    zf.write(fpath, fname)
                if os.path.exists(PHONE_CSV):
                    zf.write(PHONE_CSV, "phone.csv")
            buf.seek(0)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            await update.message.reply_document(
                document=buf,
                filename=f"tgtx_backup_{timestamp}.zip",
                caption=(
                    f"✅ *Backup Complete*\n\n"
                    f"📦 Sessions: `{len(sessions)}`\n"
                    f"🕐 Created: `{timestamp}`\n\n"
                    "_Store this zip safely — it contains your session files._"
                ),
                parse_mode="Markdown"
            )
            log_history("Backup", f"Backed up {len(sessions)} sessions")
            await msg.delete()
        except Exception as e:
            await msg.edit_text(f"❌ Backup failed: {e}")

    # ── /ban shortcut ──────────────────────────────────────────────────────
    @admin_only
    async def cmd_ban_shortcut(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        kb = self._confirm_kb("confirm_remove_banned", "back_to_main")
        await update.message.reply_text(
            "⚠️ *Remove Banned Accounts*\n\n"
            "This will scan all accounts and permanently remove banned/deactivated ones.\n\n"
            "Are you sure?",
            reply_markup=kb, parse_mode="Markdown"
        )

    # ── /limits shortcut ───────────────────────────────────────────────────
    @admin_only
    async def cmd_limits_shortcut(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        kb = self._confirm_kb("confirm_check_limits", "back_to_main")
        await update.message.reply_text(
            "⚠️ *Check & Fix Limits*\n\n"
            "This will message @SpamBot for every account and attempt to submit complaints.\n\n"
            "Are you sure?",
            reply_markup=kb, parse_mode="Markdown"
        )

    # ── /addadmin & /removeadmin ───────────────────────────────────────────
    @admin_only
    async def cmd_add_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage: `/addadmin <user_id>`", parse_mode="Markdown")
            return
        try:
            new_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID.")
            return
        if new_id in ADMIN_USER_IDS:
            await update.message.reply_text(f"ℹ️ `{new_id}` is already an admin.", parse_mode="Markdown")
            return
        ADMIN_USER_IDS.append(new_id)
        log_history("Add Admin", f"Added admin {new_id}")
        await update.message.reply_text(f"✅ `{new_id}` added as admin.", parse_mode="Markdown")

    @admin_only
    async def cmd_remove_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage: `/removeadmin <user_id>`", parse_mode="Markdown")
            return
        try:
            rem_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID.")
            return
        if rem_id == update.effective_user.id:
            await update.message.reply_text("❌ You can't remove yourself.")
            return
        if rem_id not in ADMIN_USER_IDS:
            await update.message.reply_text(f"ℹ️ `{rem_id}` is not an admin.", parse_mode="Markdown")
            return
        ADMIN_USER_IDS.remove(rem_id)
        log_history("Remove Admin", f"Removed admin {rem_id}")
        await update.message.reply_text(f"✅ `{rem_id}` removed from admins.", parse_mode="Markdown")

    # ── /config ────────────────────────────────────────────────────────────
    @admin_only
    async def cmd_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        cfg = load_config()
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("⏱ Default Delay",         callback_data="cfg_delay")],
            [InlineKeyboardButton("🕐 Auto-Scan Hour",        callback_data="cfg_scan_hour")],
            [InlineKeyboardButton("📅 Toggle Auto-Scan",      callback_data="cfg_toggle_scan")],
            [InlineKeyboardButton("🔽 Clone Filter",          callback_data="cfg_clone_filter")],
            [InlineKeyboardButton("🔔 Toggle Error Alerts",   callback_data="cfg_toggle_alerts")],
            [InlineKeyboardButton("⬅️ Back",                  callback_data="back_to_main")],
        ])
        text = (
            "⚙️ *Runtime Config*\n\n"
            f"⏱ Default delay: `{cfg['default_delay']}s`\n"
            f"🕐 Auto-scan hour: `{cfg['auto_scan_hour']}:00`\n"
            f"📅 Auto-scan: `{'ON' if cfg['auto_scan_enabled'] else 'OFF'}`\n"
            f"🔽 Clone filter: `{cfg['clone_filter']}`\n"
            f"🔔 Error alerts: `{'ON' if cfg['alert_on_error'] else 'OFF'}`\n\n"
            "Tap a setting to change it:"
        )
        await update.message.reply_text(text, reply_markup=kb, parse_mode="Markdown")

    # ── /queue ─────────────────────────────────────────────────────────────
    @admin_only
    async def cmd_queue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        active = "🔄 Running" if (self._active_task and self._active_task.is_alive()) else "✅ Idle"
        with _queue_lock:
            pending = list(_op_queue)
        if not pending:
            text = f"📋 *Operation Queue*\n\nCurrent: {active}\nQueue: Empty"
        else:
            items = "\n".join(f"`{i+1}.` {op['name']}" for i, op in enumerate(pending))
            text = f"📋 *Operation Queue*\n\nCurrent: {active}\n\nPending:\n{items}"
        await update.message.reply_text(text, parse_mode="Markdown")

    # ──────────────────────────────────────────────────────────────────────
    # CALLBACK ROUTER
    # ──────────────────────────────────────────────────────────────────────
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.from_user.id not in ADMIN_USER_IDS:
            await query.message.reply_text("❌ Unauthorized.")
            return

        data = query.data
        routes = {
            # menus
            "account_manager":        self._menu_accounts,
            "group_tools":            self._menu_groups,
            "system_tools":           self._menu_system,
            "status":                 self._show_status,
            "back_to_main":           self._back_main,
            # account actions
            "add_accounts":           self._ask_phones,
            "remove_banned":          self._confirm_remove_banned,
            "confirm_remove_banned":  lambda q, c: self._enqueue(q, c, "remove_banned"),
            "check_limits":           self._confirm_check_limits,
            "confirm_check_limits":   lambda q, c: self._enqueue(q, c, "check_limits"),
            "view_accounts":          self._show_accounts_cb,
            "health_check":           self._trigger_health_cb,
            # group tools
            "gc_cloner":              self._ask_gc_params,
            "realtime_cloner":        self._ask_realtime_params,
            "recent_groups_source":   self._show_recent_source,
            "recent_groups_target":   self._show_recent_target,
            # system
            "logs":                   self._show_logs,
            "view_history":           self._show_history_cb,
            "backup_cb":              self._backup_cb,
            "stop_operation":         self._stop_operation,
            # config
            "cfg_delay":              lambda q, c: self._ask_config_value(q, c, "default_delay"),
            "cfg_scan_hour":          lambda q, c: self._ask_config_value(q, c, "auto_scan_hour"),
            "cfg_toggle_scan":        self._toggle_auto_scan,
            "cfg_clone_filter":       self._cycle_clone_filter,
            "cfg_toggle_alerts":      self._toggle_alerts,
        }

        # handle recent_group: prefix
        if data.startswith("rg_src:"):
            group = data[7:]
            context.user_data["prefilled_source"] = group
            await self._ask_gc_params(query, context)
            return
        if data.startswith("rg_tgt:"):
            group = data[7:]
            context.user_data["prefilled_target"] = group
            await self._ask_gc_params(query, context)
            return

        handler = routes.get(data)
        if handler:
            await handler(query, context)

    # ──────────────────────────────────────────────────────────────────────
    # SUB-MENUS
    # ──────────────────────────────────────────────────────────────────────
    async def _menu_accounts(self, query, context):
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Accounts",          callback_data="add_accounts"),
             InlineKeyboardButton("📋 View Accounts",         callback_data="view_accounts")],
            [InlineKeyboardButton("🗑️ Remove Banned",         callback_data="remove_banned"),
             InlineKeyboardButton("🔍 Check Limits",          callback_data="check_limits")],
            [InlineKeyboardButton("🏥 Health Dashboard",      callback_data="health_check")],
            [InlineKeyboardButton("📦 Backup Sessions",       callback_data="backup_cb")],
            [InlineKeyboardButton("⬅️ Back",                  callback_data="back_to_main")],
        ])
        phones   = read_phones()
        sessions = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
        await query.edit_message_text(
            f"📊 *Account Manager*\n\n"
            f"📱 Accounts: `{len(phones)}` | 💾 Sessions: `{len(sessions)}`\n\n"
            "Choose an action:",
            reply_markup=kb, parse_mode="Markdown"
        )

    async def _menu_groups(self, query, context):
        cfg     = load_config()
        recent  = cfg.get("recent_groups", [])
        rows    = []
        if recent:
            rows.append([InlineKeyboardButton("🕐 Recent Groups →", callback_data="recent_groups_source")])
        rows += [
            [InlineKeyboardButton("📋 Group Cloner",       callback_data="gc_cloner"),
             InlineKeyboardButton("🔄 Real-time Cloner",   callback_data="realtime_cloner")],
            [InlineKeyboardButton("⬅️ Back",               callback_data="back_to_main")],
        ]
        await query.edit_message_text(
            "🚀 *Group Tools*\n\n"
            "• *Group Cloner:* Copy historical messages\n"
            "• *Real-time:* Forward new messages live\n"
            "• *Filter:* Set via /config (text/media/all)\n\n"
            "Choose a tool:",
            reply_markup=InlineKeyboardMarkup(rows), parse_mode="Markdown"
        )

    async def _menu_system(self, query, context):
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Logs",        callback_data="logs"),
             InlineKeyboardButton("📋 History",     callback_data="view_history")],
            [InlineKeyboardButton("📦 Backup",      callback_data="backup_cb"),
             InlineKeyboardButton("⚙️ Config",      callback_data="back_to_main")],
            [InlineKeyboardButton("⬅️ Back",        callback_data="back_to_main")],
        ])
        await query.edit_message_text(
            "⚙️ *System Tools*\n\nMonitor and maintain your bot:",
            reply_markup=kb, parse_mode="Markdown"
        )

    async def _back_main(self, query, context):
        context.user_data.clear()
        await query.edit_message_text(
            "🤖 *TGTX Main Menu*\n\nSelect an option:",
            reply_markup=self._main_kb(), parse_mode="Markdown"
        )

    # ── Status panel ───────────────────────────────────────────────────────
    async def _show_status(self, query, context):
        phones   = read_phones()
        sessions = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
        task_str = "🔄 Running" if (self._active_task and self._active_task.is_alive()) else "✅ Idle"
        cfg      = load_config()
        with _queue_lock:
            q_size = len(_op_queue)
        text = (
            "📈 *System Status*\n\n"
            f"🤖 *Bot:* ✅ Online\n"
            f"⏱ *Uptime:* `{get_uptime()}`\n"
            f"📱 *Accounts:* `{len(phones)}`\n"
            f"💾 *Sessions:* `{len(sessions)}`\n"
            f"⚙️ *Active Op:* {task_str}\n"
            f"📋 *Queue:* `{q_size}` pending\n"
            f"🕐 *Daily Scan:* {'✅ ON @ ' + str(cfg['auto_scan_hour']) + ':00' if cfg['auto_scan_enabled'] else '❌ OFF'}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "All systems operational! 🎉"
        )
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Main Menu", callback_data="back_to_main")]])
        await query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    async def _show_accounts_cb(self, query, context):
        phones = read_phones()
        if not phones:
            text = "📭 No accounts yet."
        else:
            lines = [f"📱 *Accounts ({len(phones)} total):*\n"]
            for i, p in enumerate(phones, 1):
                lines.append(f"`{i}.` {p}")
            text = "\n".join(lines)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="account_manager")]])
        await query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    async def _show_history_cb(self, query, context):
        text = "📭 No history yet."
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE) as f:
                history = json.load(f)
            if history:
                lines = ["📋 *Last 10 Operations:*\n"]
                for h in reversed(history[-10:]):
                    lines.append(f"• `{h['ts']}` — *{h['action']}*\n  _{h['detail']}_")
                text = "\n".join(lines)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="system_tools")]])
        await query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    async def _show_logs(self, query, context):
        try:
            with open(LOG_FILE) as f:
                lines = f.readlines()
            last = "".join(lines[-25:]).strip() or "No log entries yet."
        except FileNotFoundError:
            last = "Log file not found."
        text = f"📊 *Recent Logs (last 25 lines):*\n\n```\n{last[:3800]}\n```"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="system_tools")]])
        await query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    async def _backup_cb(self, query, context):
        sessions = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
        if not sessions:
            await query.edit_message_text("📭 No session files to backup.")
            return
        await query.edit_message_text(f"📦 Creating backup of `{len(sessions)}` session(s)…", parse_mode="Markdown")
        try:
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for fname in sessions:
                    zf.write(os.path.join(SESSIONS_DIR, fname), fname)
                if os.path.exists(PHONE_CSV):
                    zf.write(PHONE_CSV, "phone.csv")
            buf.seek(0)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            await query.message.reply_document(
                document=buf,
                filename=f"tgtx_backup_{ts}.zip",
                caption=f"✅ *Backup:* `{len(sessions)}` sessions — `{ts}`",
                parse_mode="Markdown"
            )
            log_history("Backup", f"Backed up {len(sessions)} sessions")
        except Exception as e:
            await query.message.reply_text(f"❌ Backup failed: {e}")

    async def _trigger_health_cb(self, query, context):
        phones = read_phones()
        if not phones:
            await query.edit_message_text("📭 No accounts to check.")
            return
        await query.edit_message_text(
            f"🏥 *Health Dashboard*\n\nChecking `{len(phones)}` accounts…\nResults will follow.",
            parse_mode="Markdown"
        )
        chat_id = query.message.chat_id
        bot     = context.bot

        async def send_update(t):
            try:
                await bot.send_message(chat_id, t, parse_mode="Markdown")
            except Exception:
                pass

        loop = asyncio.get_event_loop()
        def task():
            asyncio.run_coroutine_threadsafe(
                self._do_health_check(send_update, phones), loop
            ).result()

        self._active_task = threading.Thread(target=task, daemon=True)
        self._active_task.start()

    async def _stop_operation(self, query, context):
        _stop_event.set()
        await query.edit_message_text("🛑 *Stop signal sent.* Operation will halt after current step.")
        await asyncio.sleep(0.5)
        _stop_event.clear()

    # ── Confirm dialogs ────────────────────────────────────────────────────
    async def _confirm_remove_banned(self, query, context):
        await query.edit_message_text(
            "⚠️ *Remove Banned Accounts*\n\n"
            "This will scan all accounts and permanently remove banned/deactivated ones from phone.csv and delete their session files.\n\n"
            "Are you sure?",
            reply_markup=self._confirm_kb("confirm_remove_banned"), parse_mode="Markdown"
        )

    async def _confirm_check_limits(self, query, context):
        await query.edit_message_text(
            "⚠️ *Check & Fix Limits*\n\n"
            "This will message @SpamBot for every account and attempt to auto-submit complaints for limited accounts.\n\n"
            "Are you sure?",
            reply_markup=self._confirm_kb("confirm_check_limits"), parse_mode="Markdown"
        )

    # ── Recent groups ──────────────────────────────────────────────────────
    async def _show_recent_source(self, query, context):
        cfg    = load_config()
        recent = cfg.get("recent_groups", [])
        if not recent:
            await query.answer("No recent groups yet.", show_alert=True)
            return
        rows = [[InlineKeyboardButton(g, callback_data=f"rg_src:{g}")] for g in recent]
        rows.append([InlineKeyboardButton("⬅️ Back", callback_data="group_tools")])
        await query.edit_message_text(
            "🕐 *Select Source Group:*\n\nTap to pre-fill:",
            reply_markup=InlineKeyboardMarkup(rows), parse_mode="Markdown"
        )

    async def _show_recent_target(self, query, context):
        cfg    = load_config()
        recent = cfg.get("recent_groups", [])
        if not recent:
            await query.answer("No recent groups yet.", show_alert=True)
            return
        rows = [[InlineKeyboardButton(g, callback_data=f"rg_tgt:{g}")] for g in recent]
        rows.append([InlineKeyboardButton("⬅️ Back", callback_data="group_tools")])
        await query.edit_message_text(
            "🕐 *Select Target Group:*\n\nTap to pre-fill:",
            reply_markup=InlineKeyboardMarkup(rows), parse_mode="Markdown"
        )

    # ── Config callbacks ───────────────────────────────────────────────────
    async def _ask_config_value(self, query, context, key: str):
        labels = {
            "default_delay": ("⏱ Default Delay", "Enter new delay in seconds (e.g. 3):"),
            "auto_scan_hour": ("🕐 Auto-Scan Hour", "Enter hour 0-23 (e.g. 8 for 8:00 AM):"),
        }
        label, prompt = labels.get(key, (key, f"Enter new value for {key}:"))
        await query.edit_message_text(
            f"⚙️ *Edit Config: {label}*\n\n{prompt}",
            parse_mode="Markdown"
        )
        context.user_data["expecting_config_key"] = key

    async def _toggle_auto_scan(self, query, context):
        cfg = load_config()
        cfg["auto_scan_enabled"] = not cfg["auto_scan_enabled"]
        save_config(cfg)
        state = "ON" if cfg["auto_scan_enabled"] else "OFF"
        await query.answer(f"Daily auto-scan turned {state}.", show_alert=True)
        await self.cmd_config.__wrapped__(self, query._get_update_for_answer(), context)

    async def _cycle_clone_filter(self, query, context):
        options = ["all", "text", "media", "text+media"]
        cfg = load_config()
        cur = cfg.get("clone_filter", "all")
        nxt = options[(options.index(cur) + 1) % len(options)] if cur in options else "all"
        cfg["clone_filter"] = nxt
        save_config(cfg)
        await query.answer(f"Clone filter: {nxt}", show_alert=True)

    async def _toggle_alerts(self, query, context):
        cfg = load_config()
        cfg["alert_on_error"] = not cfg["alert_on_error"]
        save_config(cfg)
        state = "ON" if cfg["alert_on_error"] else "OFF"
        await query.answer(f"Error alerts turned {state}.", show_alert=True)

    # ──────────────────────────────────────────────────────────────────────
    # OPERATION QUEUE RUNNER
    # ──────────────────────────────────────────────────────────────────────
    async def _enqueue(self, query, context, command: str):
        chat_id = query.message.chat_id
        stop_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🛑 Stop", callback_data="stop_operation")]])

        async def send_update(t):
            try:
                await context.bot.send_message(chat_id, t, parse_mode="Markdown")
            except Exception as e:
                logger.warning(f"send_update error: {e}")

        loop = asyncio.get_event_loop()

        if command == "remove_banned":
            coro_fn = self._do_remove_banned
        elif command == "check_limits":
            coro_fn = self._do_check_limits
        else:
            return

        # If something is running, queue it
        if self._active_task and self._active_task.is_alive():
            with _queue_lock:
                _op_queue.append({"name": command.replace("_", " ").title(), "fn": coro_fn, "su": send_update, "loop": loop})
            await query.edit_message_text(
                f"📋 *Queued:* `{command.replace('_', ' ').title()}`\n\nAnother operation is running. This will start automatically when it finishes.",
                reply_markup=stop_kb, parse_mode="Markdown"
            )
            return

        await query.edit_message_text(
            f"🔄 *Starting {command.replace('_', ' ').title()}…*\nLive updates will follow.",
            reply_markup=stop_kb, parse_mode="Markdown"
        )

        def task():
            asyncio.run_coroutine_threadsafe(coro_fn(send_update), loop).result()
            # run next in queue
            with _queue_lock:
                if _op_queue:
                    nxt = _op_queue.pop(0)
            if _op_queue is not None and 'nxt' in dir():
                asyncio.run_coroutine_threadsafe(
                    nxt["su"](f"▶️ *Starting queued op:* `{nxt['name']}`"), nxt["loop"]
                ).result()
                asyncio.run_coroutine_threadsafe(nxt["fn"](nxt["su"]), nxt["loop"]).result()

        self._active_task = threading.Thread(target=task, daemon=True)
        self._active_task.start()

    # ──────────────────────────────────────────────────────────────────────
    # ADD ACCOUNTS
    # ──────────────────────────────────────────────────────────────────────
    async def _ask_phones(self, query, context):
        await query.edit_message_text(
            "📱 *Add Accounts*\n\n"
            "Send phone numbers in this format:\n"
            "```\n3\n+1234567890\n+1234567891\n+1234567892\n```\n"
            "First line = count, then one number per line with country code.",
            parse_mode="Markdown"
        )
        context.user_data["expecting_phones"] = True

    async def _process_phones(self, update: Update, text: str):
        lines = text.strip().splitlines()
        try:
            count   = int(lines[0])
            numbers = [l.strip() for l in lines[1:count + 1] if l.strip()]
            if len(numbers) != count:
                await update.message.reply_text("❌ Count doesn't match the number of lines.")
                return
        except (ValueError, IndexError):
            await update.message.reply_text("❌ Invalid format — first line must be a number.")
            return

        existing   = set(read_phones())
        new        = [n for n in numbers if n not in existing]
        duplicates = count - len(new)

        if not new:
            await update.message.reply_text("ℹ️ All numbers already exist — nothing to add.")
            return

        msg = await update.message.reply_text(
            f"🔄 Logging in `{len(new)}` new account(s)…", parse_mode="Markdown"
        )
        errors = []
        added  = []

        for phone_raw in new:
            if _stop_event.is_set():
                break
            try:
                from pyrogram import Client as PyroClient
                phone = parse_phone(phone_raw)
                app   = PyroClient(
                    f"{SESSIONS_DIR}/{phone}",
                    api_id=int(API_ID), api_hash=API_HASH, phone_number=phone
                )
                app.start()
                try:
                    app.join_chat("@The_Hacking_Zone")
                    time.sleep(2)
                except Exception:
                    pass
                app.stop()
                added.append(phone_raw)
                logger.info(f"Logged in: {phone}")
            except Exception as e:
                errors.append(f"{phone_raw}: {str(e)[:60]}")
                logger.warning(f"Login failed {phone_raw}: {e}")

        write_phones(read_phones() + added)
        log_history("Add Accounts", f"Added:{len(added)} Failed:{len(errors)} Dupes:{duplicates}")

        result = (
            f"✅ *Add Accounts Complete*\n\n"
            f"✔️ Added: `{len(added)}`\n"
            f"⚠️ Failed: `{len(errors)}`\n"
            f"🔁 Duplicates skipped: `{duplicates}`"
        )
        if errors:
            result += "\n\n*Errors:*\n" + "\n".join(f"• {e}" for e in errors[:5])
        result += "\n\nUse /menu to return."
        await msg.edit_text(result, parse_mode="Markdown")

    # ──────────────────────────────────────────────────────────────────────
    # REMOVE BANNED
    # ──────────────────────────────────────────────────────────────────────
    async def _do_remove_banned(self, send_update):
        from pyrogram import Client as PyroClient
        from pyrogram.errors import (
            AuthKeyUnregistered, UserDeactivatedBan,
            SessionExpired, SessionRevoked, UserDeactivated
        )
        phones = read_phones()
        if not phones:
            await send_update("📭 No accounts in phone.csv.")
            return

        await send_update(f"🔍 Scanning `{len(phones)}` account(s) for bans…")
        banned = []
        active = []

        for i, phone_raw in enumerate(phones, 1):
            if _stop_event.is_set():
                await send_update("🛑 Stopped by user.")
                break
            phone = parse_phone(phone_raw)
            try:
                app = PyroClient(
                    f"{SESSIONS_DIR}/{phone}",
                    api_id=int(API_ID), api_hash=API_HASH, phone_number=phone
                )
                app.start()
                app.stop()
                active.append(phone_raw)
            except (AuthKeyUnregistered, UserDeactivatedBan, SessionExpired, SessionRevoked, UserDeactivated) as e:
                banned.append(phone_raw)
                sp = f"{SESSIONS_DIR}/{phone}.session"
                if os.path.exists(sp):
                    os.remove(sp)
                await send_update(f"⛔ `{phone}` — {type(e).__name__} — removed")
                logger.info(f"Banned removed: {phone}")
            except Exception as e:
                active.append(phone_raw)
                logger.warning(f"Scan error {phone}: {e}")

            if i % 5 == 0:
                await send_update(f"⏳ Progress: `{i}/{len(phones)}`…")

        write_phones(active)
        log_history("Remove Banned", f"Removed:{len(banned)} Active:{len(active)}")
        cfg = load_config()
        if cfg.get("alert_on_error") and banned:
            pass  # alert already sent per-account above

        await send_update(
            f"✅ *Ban Scan Complete*\n\n"
            f"⛔ Removed: `{len(banned)}`\n"
            f"✔️ Active: `{len(active)}`\n\n"
            f"Use /menu to continue."
        )

    # ──────────────────────────────────────────────────────────────────────
    # CHECK & FIX LIMITS
    # ──────────────────────────────────────────────────────────────────────
    async def _do_check_limits(self, send_update):
        from pyrogram import Client as PyroClient

        phones = read_phones()
        if not phones:
            await send_update("📭 No accounts in phone.csv.")
            return

        await send_update(f"🔍 Checking limits on `{len(phones)}` account(s) via @SpamBot…")

        try:
            import requests as req
            content = req.get("https://pastebin.com/raw/YKbeUazQ", timeout=10).text
        except Exception:
            content = "I'm not a spammer."

        results = {"no_limit": [], "fixed": [], "limited": [], "error": []}
        FREE    = "Good news, no limits"
        HARSH   = "some phone numbers may trigger"
        LIMITED = "some actions can trigger a harsh response"

        for i, phone_raw in enumerate(phones, 1):
            if _stop_event.is_set():
                await send_update("🛑 Stopped by user.")
                break
            phone = parse_phone(phone_raw)
            try:
                app = PyroClient(
                    f"{SESSIONS_DIR}/{phone}",
                    api_id=int(API_ID), api_hash=API_HASH, phone_number=phone
                )
                app.start()
                app.send_message("spambot", "/start")
                time.sleep(1.5)
                last = next(app.get_chat_history("spambot", limit=1), None)
                txt  = (last.text or "") if last else ""

                if FREE in txt:
                    results["no_limit"].append(phone)
                    await send_update(f"✅ `{phone}` — No limit")

                elif HARSH in txt:
                    app.send_message("spambot", "Submit a complaint")
                    time.sleep(1)
                    r2 = next(app.get_chat_history("spambot", limit=1), None)
                    if r2 and "confirm" in (r2.text or "").lower():
                        app.send_message("spambot", "No, I'll never do any of this!")
                        time.sleep(1)
                        app.send_message("spambot", content)
                        time.sleep(1)
                    results["fixed"].append(phone)
                    await send_update(f"⚠️ `{phone}` — Harsh flag, complaint submitted")

                elif LIMITED in txt:
                    app.send_message("spambot", "This is a mistake")
                    time.sleep(1)
                    r2 = next(app.get_chat_history("spambot", limit=1), None)
                    if r2 and "complaint" in (r2.text or "").lower():
                        app.send_message("spambot", "Yes")
                        time.sleep(1)
                        app.send_message("spambot", "No! Never did that!")
                        time.sleep(1)
                        app.send_message("spambot", content)
                        time.sleep(1)
                    results["limited"].append(phone)
                    await send_update(f"🔴 `{phone}` — Limited, complaint submitted")

                else:
                    results["error"].append(phone)
                    await send_update(f"❓ `{phone}` — Unknown SpamBot response")

                app.stop()

            except Exception as e:
                results["error"].append(phone)
                cfg = load_config()
                if cfg.get("alert_on_error"):
                    await send_update(f"⚠️ Error on `{phone}`: `{str(e)[:80]}`")
                logger.warning(f"Limit check error {phone}: {e}")

            if i % 3 == 0:
                await send_update(f"⏳ Progress: `{i}/{len(phones)}`…")

        log_history(
            "Check Limits",
            f"OK:{len(results['no_limit'])} Fixed:{len(results['fixed'])} "
            f"Limited:{len(results['limited'])} Error:{len(results['error'])}"
        )
        await send_update(
            f"✅ *Limit Check Complete*\n\n"
            f"✔️ No limit: `{len(results['no_limit'])}`\n"
            f"🔧 Fixed: `{len(results['fixed'])}`\n"
            f"🔴 Still limited: `{len(results['limited'])}`\n"
            f"❓ Errors: `{len(results['error'])}`\n\n"
            f"Use /menu to continue."
        )

    # ──────────────────────────────────────────────────────────────────────
    # GROUP CLONER — ask params
    # ──────────────────────────────────────────────────────────────────────
    async def _ask_gc_params(self, query, context):
        pre_src = context.user_data.pop("prefilled_source", "")
        pre_tgt = context.user_data.pop("prefilled_target", "")
        cfg     = load_config()
        example = (
            f"{pre_src or '@oldgroup'}\n"
            f"{pre_tgt or '@newgroup'}\n"
            "100\n2\n2024-01-01\n2024-12-31\n2"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🕐 Recent: Source", callback_data="recent_groups_source"),
             InlineKeyboardButton("🕐 Recent: Target", callback_data="recent_groups_target")],
            [InlineKeyboardButton("⬅️ Back", callback_data="group_tools")],
        ])
        await query.edit_message_text(
            "📋 *Group Cloner Setup*\n\n"
            f"Current filter: `{cfg['clone_filter']}` (change via /config)\n\n"
            "Send parameters — one per line:\n"
            "```\nsource_group\ntarget_group\nmessage_count\n"
            "delay_seconds\nstart_date (blank=all)\nend_date (blank=latest)\nadmin_count\n```\n"
            f"Example:\n```\n{example}\n```",
            reply_markup=kb, parse_mode="Markdown"
        )
        context.user_data["expecting_gc_params"] = True

    async def _ask_realtime_params(self, query, context):
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="group_tools")]])
        cfg = load_config()
        await query.edit_message_text(
            "🔄 *Real-time Cloner Setup*\n\n"
            f"Current filter: `{cfg['clone_filter']}` (change via /config)\n\n"
            "Send parameters — one per line:\n"
            "```\nsource_group\ntarget_group\ninitial_message_count\n"
            "delay_seconds\nstart_date (blank=all)\nend_date (blank=latest)\nadmin_count\n```",
            reply_markup=kb, parse_mode="Markdown"
        )
        context.user_data["expecting_realtime_params"] = True

    def _parse_cloner_params(self, lines: list[str]) -> dict | None:
        if len(lines) < 4:
            return None
        try:
            return {
                "source_group": lines[0].strip(),
                "target_group": lines[1].strip(),
                "msg_count":    int(lines[2].strip()),
                "delay":        int(lines[3].strip()),
                "start_date":   lines[4].strip() if len(lines) > 4 else "",
                "end_date":     lines[5].strip() if len(lines) > 5 else "",
                "admin_count":  int(lines[6].strip()) if len(lines) > 6 and lines[6].strip() else 1,
            }
        except (ValueError, IndexError):
            return None

    async def _process_gc_params(self, update: Update, text: str):
        params = self._parse_cloner_params(text.strip().splitlines())
        if not params:
            await update.message.reply_text("❌ Invalid format. Check the example and try again.")
            return
        phones = read_phones()
        if not phones:
            await update.message.reply_text("❌ No accounts in phone.csv.")
            return
        _add_recent_group(params["source_group"])
        _add_recent_group(params["target_group"])
        bot     = context = update.get_bot()
        chat_id = update.message.chat_id
        await update.message.reply_text(
            f"🔄 *Group Cloner Starting…*\n\n"
            f"Source: `{params['source_group']}`\n"
            f"Target: `{params['target_group']}`\n"
            f"Messages: `{params['msg_count']}` | Delay: `{params['delay']}s`\n\n"
            "_Live updates to follow…_",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛑 Stop", callback_data="stop_operation")]])
        )

        async def send_update(t):
            try:
                await bot.send_message(chat_id, t, parse_mode="Markdown")
            except Exception:
                pass

        loop = asyncio.get_event_loop()
        def task():
            asyncio.run_coroutine_threadsafe(
                self._do_gc_clone(send_update, phones, params, realtime=False), loop
            ).result()
        self._active_task = threading.Thread(target=task, daemon=True)
        self._active_task.start()

    async def _process_realtime_params(self, update: Update, text: str):
        params = self._parse_cloner_params(text.strip().splitlines())
        if not params:
            await update.message.reply_text("❌ Invalid format. Check the example and try again.")
            return
        phones = read_phones()
        if not phones:
            await update.message.reply_text("❌ No accounts in phone.csv.")
            return
        _add_recent_group(params["source_group"])
        _add_recent_group(params["target_group"])
        bot     = update.get_bot()
        chat_id = update.message.chat_id
        await update.message.reply_text(
            f"🔴 *Real-time Cloner Starting…*\n\n"
            f"Source: `{params['source_group']}`\n"
            f"Target: `{params['target_group']}`\n"
            f"Initial: `{params['msg_count']}` msgs | Delay: `{params['delay']}s`\n\n"
            "_Runs continuously. Use /cancel to stop._",
            parse_mode="Markdown"
        )

        async def send_update(t):
            try:
                await bot.send_message(chat_id, t, parse_mode="Markdown")
            except Exception:
                pass

        loop = asyncio.get_event_loop()
        def task():
            asyncio.run_coroutine_threadsafe(
                self._do_gc_clone(send_update, phones, params, realtime=True), loop
            ).result()
        self._active_task = threading.Thread(target=task, daemon=True)
        self._active_task.start()

    # ──────────────────────────────────────────────────────────────────────
    # CORE CLONER LOGIC
    # ──────────────────────────────────────────────────────────────────────
    async def _do_gc_clone(self, send_update, phones: list[str], params: dict, realtime: bool):
        from pyrogram import Client as PyroClient, filters as pyro_filters
        from pyrogram.errors import UserAlreadyParticipant
        from pyrogram.handlers import MessageHandler as PyroMH
        from pyrogram.enums import ChatMembersFilter
        from datetime import datetime as dt

        groupsc     = params["source_group"]
        groupyour   = params["target_group"]
        msg_count   = params["msg_count"]
        delay       = params["delay"]
        admin_count = max(1, min(params["admin_count"], len(phones)))
        cfg         = load_config()
        clone_filter = cfg.get("clone_filter", "all")

        start_ts = end_ts = None
        for key, attr in [("start_date", "start_ts"), ("end_date", "end_ts")]:
            val = params.get(key, "")
            if val:
                try:
                    locals()[attr] if False else None
                    ts = int(dt.strptime(val, "%Y-%m-%d").timestamp())
                    if key == "start_date":
                        start_ts = ts
                    else:
                        end_ts = ts
                except ValueError:
                    await send_update(f"⚠️ Invalid {key} — ignoring.")

        # ── Scout: scrape & detect admins ─────────────────────────────────
        scout_phone = parse_phone(phones[0])
        scout = PyroClient(
            f"{SESSIONS_DIR}/{scout_phone}",
            api_id=int(API_ID), api_hash=API_HASH, phone_number=scout_phone
        )
        scout.start()
        try:
            scout.join_chat(groupsc)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            await send_update(f"❌ Cannot join source: {e}")
            scout.stop()
            return

        admin_ids = set()
        try:
            for m in scout.get_chat_members(groupsc, filter=ChatMembersFilter.ADMINISTRATORS):
                admin_ids.add(m.user.id)
        except Exception as e:
            await send_update(f"⚠️ Admin list unavailable: {e}")

        await send_update(f"📡 Scraping `{msg_count}` messages from `{groupsc}` (filter: `{clone_filter}`)…")

        def _passes_filter(m) -> bool:
            if clone_filter == "all":
                return True
            has_text  = bool(m.text)
            has_media = bool(m.photo or m.video or m.document or m.sticker or m.animation)
            if clone_filter == "text":
                return has_text
            if clone_filter == "media":
                return has_media
            if clone_filter == "text+media":
                return has_text or has_media
            return True

        messages = []
        for m in scout.get_chat_history(groupsc, limit=msg_count):
            ts = m.date.timestamp()
            if start_ts and ts < start_ts:
                continue
            if end_ts and ts > end_ts:
                continue
            if _passes_filter(m):
                messages.append(m)
        messages.reverse()

        message_data = [(m.id, (not m.from_user) or (m.from_user.id in admin_ids)) for m in messages]
        scout.stop()

        await send_update(
            f"✅ Scraped `{len(message_data)}` messages after filter.\n"
            f"Joining all accounts to both groups…"
        )

        admin_phones   = [parse_phone(phones[i]) for i in range(admin_count)]
        regular_phones = [parse_phone(p) for p in phones[admin_count:]] or admin_phones

        for phone_raw in phones:
            if _stop_event.is_set():
                break
            phone = parse_phone(phone_raw)
            try:
                app = PyroClient(f"{SESSIONS_DIR}/{phone}", api_id=int(API_ID), api_hash=API_HASH, phone_number=phone)
                app.start()
                for g in (groupsc, groupyour):
                    try:
                        app.join_chat(g)
                    except UserAlreadyParticipant:
                        pass
                app.stop()
            except Exception as e:
                logger.warning(f"Join failed {phone}: {e}")

        await send_update(
            f"📌 *Make sure these are admins in `{groupyour}`:*\n"
            + "\n".join(f"• `{p}`" for p in admin_phones)
            + "\n\n_Proceeding in 10 seconds…_"
        )
        time.sleep(10)

        # ── Send messages ──────────────────────────────────────────────────
        await send_update(f"📤 Sending `{len(message_data)}` messages…")
        ai = ri = sent = failed = 0
        t_start = time.time()

        for i, (msg_id, is_admin) in enumerate(message_data, 1):
            if _stop_event.is_set():
                await send_update("🛑 Stopped by user.")
                break
            phone = admin_phones[ai % len(admin_phones)] if is_admin else regular_phones[ri % len(regular_phones)]
            if is_admin:
                ai += 1
            else:
                ri += 1
            try:
                app = PyroClient(f"{SESSIONS_DIR}/{phone}", api_id=int(API_ID), api_hash=API_HASH, phone_number=phone)
                app.start()
                time.sleep(delay)
                app.copy_message(groupyour, groupsc, msg_id)
                app.stop()
                sent += 1
            except Exception as e:
                failed += 1
                logger.warning(f"Copy failed msg {msg_id}: {e}")
                cfg = load_config()
                if cfg.get("alert_on_error"):
                    await send_update(f"⚠️ Failed msg `{msg_id}`: `{str(e)[:60]}`")

            if i % 20 == 0:
                elapsed = int(time.time() - t_start)
                rate    = sent / elapsed if elapsed else 0
                await send_update(
                    f"⏳ Progress: `{i}/{len(message_data)}`\n"
                    f"✔️ `{sent}` ❌ `{failed}` | ⚡ `{rate:.1f}` msg/s"
                )

        elapsed = int(time.time() - t_start)
        rate    = sent / elapsed if elapsed else 0

        if not realtime:
            log_history("GC Clone", f"Cloned:{sent} Failed:{failed} {groupsc}→{groupyour} ({elapsed}s)")
            await send_update(
                f"🎉 *Clone Complete!*\n\n"
                f"✔️ Sent: `{sent}` | ❌ Failed: `{failed}`\n"
                f"⏱ Time: `{elapsed}s` | ⚡ Rate: `{rate:.1f}` msg/s\n\n"
                f"Use /menu to continue."
            )
            return

        # ── Real-time monitoring ───────────────────────────────────────────
        await send_update(
            f"🔴 *Real-time monitoring active*\n"
            f"Source: `{groupsc}` → Target: `{groupyour}`\n"
            f"Filter: `{clone_filter}` | Use /cancel to stop."
        )

        last_id = message_data[-1][0] if message_data else 0
        monitor_phone = parse_phone(phones[0])
        monitor_app   = PyroClient(
            f"{SESSIONS_DIR}/{monitor_phone}",
            api_id=int(API_ID), api_hash=API_HASH, phone_number=monitor_phone
        )
        monitor_app.start()
        rt_sent = rt_failed = 0

        def rt_handler(client, message):
            nonlocal last_id, ai, ri, rt_sent, rt_failed
            if message.id <= last_id or _stop_event.is_set():
                return
            if not _passes_filter(message):
                return
            last_id  = message.id
            is_admin = (not message.from_user) or (message.from_user.id in admin_ids)
            phone    = admin_phones[ai % len(admin_phones)] if is_admin else regular_phones[ri % len(regular_phones)]
            if is_admin:
                ai += 1
            else:
                ri += 1
            try:
                fwd = PyroClient(f"{SESSIONS_DIR}/{phone}", api_id=int(API_ID), api_hash=API_HASH, phone_number=phone)
                fwd.start()
                time.sleep(delay)
                fwd.copy_message(groupyour, groupsc, message.id)
                fwd.stop()
                rt_sent += 1
            except Exception as e:
                rt_failed += 1
                logger.warning(f"RT forward failed: {e}")

        monitor_app.add_handler(PyroMH(rt_handler, pyro_filters.chat(groupsc)))

        try:
            while not _stop_event.is_set():
                time.sleep(1)
        finally:
            monitor_app.stop()
            log_history("RT Clone", f"Forwarded:{rt_sent} Failed:{rt_failed} {groupsc}→{groupyour}")
            asyncio.run_coroutine_threadsafe(
                send_update(
                    f"🛑 *Real-time stopped*\n\n"
                    f"✔️ Forwarded: `{rt_sent}` | ❌ Failed: `{rt_failed}`"
                ), asyncio.get_event_loop()
            )

    # ──────────────────────────────────────────────────────────────────────
    # DAILY AUTO-SCAN JOB
    # ──────────────────────────────────────────────────────────────────────
    async def _job_daily_scan(self, context: ContextTypes.DEFAULT_TYPE):
        logger.info("Running scheduled daily scan…")
        phones = read_phones()
        if not phones:
            return

        report_lines = [
            f"📅 *Daily Auto-Scan Report*\n`{datetime.now().strftime('%Y-%m-%d %H:%M')}`\n"
        ]

        # quick health pass
        from pyrogram import Client as PyroClient
        from pyrogram.errors import (
            AuthKeyUnregistered, UserDeactivatedBan,
            SessionExpired, SessionRevoked, UserDeactivated
        )
        active = banned = limited = 0
        for phone_raw in phones:
            phone = parse_phone(phone_raw)
            try:
                app = PyroClient(
                    f"{SESSIONS_DIR}/{phone}",
                    api_id=int(API_ID), api_hash=API_HASH, phone_number=phone
                )
                app.start()
                app.send_message("spambot", "/start")
                time.sleep(1)
                last = next(app.get_chat_history("spambot", limit=1), None)
                txt  = (last.text or "") if last else ""
                app.stop()
                if "Good news" in txt:
                    active += 1
                elif "limited" in txt.lower() or "actions can trigger" in txt.lower():
                    limited += 1
                else:
                    active += 1
            except (AuthKeyUnregistered, UserDeactivatedBan, SessionExpired, SessionRevoked, UserDeactivated):
                banned += 1
            except Exception:
                active += 1

        report_lines += [
            f"📱 Total accounts: `{len(phones)}`",
            f"✅ Active: `{active}`",
            f"⚠️ Limited: `{limited}`",
            f"⛔ Banned: `{banned}`\n",
        ]

        # last 5 history entries
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE) as f:
                hist = json.load(f)
            if hist:
                report_lines.append("*Recent Ops:*")
                for h in reversed(hist[-5:]):
                    report_lines.append(f"• `{h['ts']}` {h['action']} — {h['detail']}")

        report_lines.append("\n_Use /health for a full breakdown._")
        report = "\n".join(report_lines)

        log_history("Daily Scan", f"Active:{active} Limited:{limited} Banned:{banned}")

        for uid in ADMIN_USER_IDS:
            try:
                await context.bot.send_message(uid, report, parse_mode="Markdown")
            except Exception as e:
                logger.warning(f"Could not send daily report to {uid}: {e}")

    # ──────────────────────────────────────────────────────────────────────
    # MESSAGE ROUTER
    # ──────────────────────────────────────────────────────────────────────
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_USER_IDS:
            return
        text = update.message.text

        if context.user_data.pop("expecting_phones", False):
            await self._process_phones(update, text)

        elif context.user_data.pop("expecting_gc_params", False):
            await self._process_gc_params(update, text)

        elif context.user_data.pop("expecting_realtime_params", False):
            await self._process_realtime_params(update, text)

        elif context.user_data.pop("expecting_config_key", None) as key:
            await self._save_config_value(update, key, text)

        else:
            await update.message.reply_text(
                "ℹ️ No operation active. Use /menu to access controls.",
                parse_mode="Markdown"
            )

    async def _save_config_value(self, update: Update, key: str, text: str):
        try:
            val = int(text.strip())
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number.")
            return
        cfg = load_config()
        cfg[key] = val
        save_config(cfg)
        await update.message.reply_text(
            f"✅ *Config updated:* `{key}` = `{val}`\n\nUse /config to view all settings.",
            parse_mode="Markdown"
        )
        log_history("Config Edit", f"{key} set to {val}")

    # ──────────────────────────────────────────────────────────────────────
    # RUN
    # ──────────────────────────────────────────────────────────────────────
    def run(self):
        logger.info("🚀 TGTX Bot v4.0 starting…")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# ══════════════════════════════════════════════════════════════════════════════
def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise SystemExit("❌ BOT_TOKEN not set. Set the BOT_TOKEN environment variable.")
    TGTXBot(BOT_TOKEN).run()


if __name__ == "__main__":
    main()