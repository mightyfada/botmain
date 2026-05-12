import os
import asyncio
import logging
import csv
import time
import threading
import json
from datetime import datetime
from io import StringIO

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, JobQueue
)

# ── Configuration ─────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_USER_IDS = [
    int(x.strip())
    for x in os.environ.get("ADMIN_USER_IDS", "5011045316").split(",")
    if x.strip()
]
API_ID   = os.environ.get("API_ID",   "23269382")
API_HASH = os.environ.get("API_HASH", "fe19c565fb4378bd5128885428ff8e26")

DATA_DIR     = os.environ.get("DATA_DIR", ".")          # set to /data on Railway with Volume
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")
PHONE_CSV    = os.path.join(DATA_DIR, "phone.csv")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
LOG_FILE     = os.path.join(DATA_DIR, "bot.log")

os.makedirs(SESSIONS_DIR, exist_ok=True)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE),
    ],
)
logger = logging.getLogger(__name__)

# ── Operation stop flag (used to cancel long-running tasks) ───────────────────
_stop_event = threading.Event()

# ── History helpers ────────────────────────────────────────────────────────────
def log_history(action: str, detail: str):
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE) as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append({
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "detail": detail,
    })
    history = history[-50:]          # keep last 50 entries
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ── Phone CSV helpers ──────────────────────────────────────────────────────────
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

# ── Pyrogram / telethon helpers ────────────────────────────────────────────────
def parse_phone(raw: str) -> str:
    """Strip non-digit chars keeping leading + sign."""
    from telethon import utils as tu
    try:
        return tu.parse_phone(raw)
    except Exception:
        return raw.strip().lstrip("+")

# ── Admin check decorator ──────────────────────────────────────────────────────
def admin_only(func):
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = (update.effective_user or update.callback_query.from_user).id
        if uid not in ADMIN_USER_IDS:
            target = update.message or (update.callback_query and update.callback_query.message)
            if target:
                await target.reply_text("❌ Unauthorized access.")
            return
        return await func(self, update, context)
    wrapper.__name__ = func.__name__
    return wrapper

# ══════════════════════════════════════════════════════════════════════════════
class TGTXBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(token).build()
        self._setup_handlers()
        self._active_task: threading.Thread | None = None

    # ── Handler registration ───────────────────────────────────────────────
    def _setup_handlers(self):
        add = self.application.add_handler
        add(CommandHandler("start",   self.cmd_start))
        add(CommandHandler("menu",    self.cmd_menu))
        add(CommandHandler("status",  self.cmd_status))
        add(CommandHandler("cancel",  self.cmd_cancel))
        add(CommandHandler("help",    self.cmd_help))
        add(CommandHandler("history", self.cmd_history))
        add(CommandHandler("accounts",self.cmd_accounts))
        add(CallbackQueryHandler(self.button_handler))
        add(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    # ── Keyboards ──────────────────────────────────────────────────────────
    @staticmethod
    def _main_kb():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Account Manager", callback_data="account_manager")],
            [InlineKeyboardButton("🚀 Group Tools",     callback_data="group_tools")],
            [InlineKeyboardButton("⚙️ System Tools",    callback_data="system_tools")],
            [InlineKeyboardButton("📈 Status",          callback_data="status")],
        ])

    # ── /start ─────────────────────────────────────────────────────────────
    @admin_only
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        username = update.effective_user.first_name or "Admin"
        text = (
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🚀 *TGTX Bot Controller v3.0*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👋 Welcome, *{username}*\\!\n\n"
            "🎯 *Features:*\n"
            "• Multi\\-Account Management\n"
            "• Group Cloning & Migration\n"
            "• Real\\-time Message Forwarding\n"
            "• Limit Checker & Auto\\-Removal\n"
            "• Ban Detection & Cleanup\n"
            "• Operation History\n\n"
            "⚡ *Status:* ACTIVE & READY\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Select an option below:"
        )
        await update.message.reply_text(text, reply_markup=self._main_kb(), parse_mode="MarkdownV2")

    # ── /menu ──────────────────────────────────────────────────────────────
    @admin_only
    async def cmd_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        text = (
            "🤖 *TGTX Main Menu*\n\n"
            "📋 *Quick Commands:*\n"
            "• /start — Welcome banner\n"
            "• /menu — This menu\n"
            "• /status — Quick status\n"
            "• /accounts — List all accounts\n"
            "• /history — Last 10 operations\n"
            "• /cancel — Cancel current operation\n\n"
            "Select an option below:"
        )
        await update.message.reply_text(text, reply_markup=self._main_kb(), parse_mode="Markdown")

    # ── /status ────────────────────────────────────────────────────────────
    @admin_only
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        phones   = read_phones()
        task_str = "🔄 Running" if (self._active_task and self._active_task.is_alive()) else "✅ Idle"
        text = (
            "📈 *Quick Status*\n\n"
            f"🤖 Bot: ✅ Online\n"
            f"📱 Accounts: `{len(phones)}`\n"
            f"⚙️ Operation: {task_str}\n\n"
            "Use /menu for full controls."
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    # ── /cancel ────────────────────────────────────────────────────────────
    @admin_only
    async def cmd_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        _stop_event.set()
        await update.message.reply_text(
            "❌ *Operation Cancelled*\n\nAll pending operations stopped.\nUse /menu to start fresh\\!",
            parse_mode="Markdown"
        )
        _stop_event.clear()

    # ── /help ──────────────────────────────────────────────────────────────
    @admin_only
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = (
            "📚 *TGTX Bot Help*\n\n"
            "🎯 *Commands:*\n"
            "/start — Welcome banner & menu\n"
            "/menu — Main control menu\n"
            "/status — Quick status overview\n"
            "/accounts — List all accounts with index\n"
            "/history — Last 10 completed operations\n"
            "/cancel — Stop current operation\n"
            "/help — This message\n\n"
            "💡 *Tips:*\n"
            "• /cancel stops any running task mid\\-way\n"
            "• Long operations send live progress updates\n"
            "• All ops are logged in /history\n\n"
            "🔧 *Features:*\n"
            "• Multi\\-account management\n"
            "• Group cloning & migration\n"
            "• Real\\-time message forwarding\n"
            "• Automated limit checking & removal\n"
            "• Ban detection & cleanup\n"
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    # ── /history ───────────────────────────────────────────────────────────
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
        lines = ["📋 *Last Operations:*\n"]
        for h in reversed(history[-10:]):
            lines.append(f"• `{h['ts']}` — *{h['action']}*\n  {h['detail']}")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

    # ── /accounts ──────────────────────────────────────────────────────────
    @admin_only
    async def cmd_accounts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        phones = read_phones()
        if not phones:
            await update.message.reply_text("📭 No accounts in phone.csv yet.")
            return
        lines = [f"📱 *Accounts ({len(phones)} total):*\n"]
        for i, p in enumerate(phones, 1):
            lines.append(f"`{i}.` {p}")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

    # ── Callback router ────────────────────────────────────────────────────
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.from_user.id not in ADMIN_USER_IDS:
            await query.message.reply_text("❌ Unauthorized.")
            return

        data = query.data
        routes = {
            "account_manager":   self._menu_accounts,
            "group_tools":       self._menu_groups,
            "system_tools":      self._menu_system,
            "status":            self._show_status,
            "back_to_main":      self._back_main,
            "add_accounts":      self._ask_phones,
            "remove_banned":     lambda q, c: self._run_in_thread(q, c, "remove_banned"),
            "check_limits":      lambda q, c: self._run_in_thread(q, c, "check_limits"),
            "gc_cloner":         self._ask_gc_params,
            "realtime_cloner":   self._ask_realtime_params,
            "stop_operation":    self._stop_operation,
            "logs":              self._show_logs,
            "view_accounts":     self._show_accounts_cb,
            "view_history":      self._show_history_cb,
        }
        handler = routes.get(data)
        if handler:
            await handler(query, context)

    # ── Sub-menus ──────────────────────────────────────────────────────────
    async def _menu_accounts(self, query, context):
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Accounts",           callback_data="add_accounts")],
            [InlineKeyboardButton("🗑️ Remove Banned Numbers",  callback_data="remove_banned")],
            [InlineKeyboardButton("🔍 Check & Fix Limits",     callback_data="check_limits")],
            [InlineKeyboardButton("📋 View Accounts",          callback_data="view_accounts")],
            [InlineKeyboardButton("⬅️ Back",                   callback_data="back_to_main")],
        ])
        await query.edit_message_text(
            "📊 *Account Manager*\n\nManage your Telegram accounts:",
            reply_markup=kb, parse_mode="Markdown"
        )

    async def _menu_groups(self, query, context):
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Group Cloner",            callback_data="gc_cloner")],
            [InlineKeyboardButton("🔄 Real-time Cloner",        callback_data="realtime_cloner")],
            [InlineKeyboardButton("⬅️ Back",                    callback_data="back_to_main")],
        ])
        await query.edit_message_text(
            "🚀 *Group Tools*\n\n"
            "• *Group Cloner:* Copy historical messages between groups\n"
            "• *Real-time Cloner:* Live message forwarding as they arrive",
            reply_markup=kb, parse_mode="Markdown"
        )

    async def _menu_system(self, query, context):
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Logs",            callback_data="logs")],
            [InlineKeyboardButton("📋 History",         callback_data="view_history")],
            [InlineKeyboardButton("⬅️ Back",            callback_data="back_to_main")],
        ])
        await query.edit_message_text(
            "⚙️ *System Tools*\n\nView logs and operation history:",
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
        task_str = "🔄 Running" if (self._active_task and self._active_task.is_alive()) else "✅ Idle"
        # Count sessions on disk
        session_files = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
        text = (
            "📈 *System Status*\n\n"
            f"🤖 *Bot:* ✅ Online\n"
            f"📱 *Accounts in CSV:* `{len(phones)}`\n"
            f"💾 *Session Files:* `{len(session_files)}`\n"
            f"⚙️ *Current Op:* {task_str}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "All systems operational! 🎉"
        )
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Main Menu", callback_data="back_to_main")]])
        await query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    # ── Accounts view (callback) ───────────────────────────────────────────
    async def _show_accounts_cb(self, query, context):
        phones = read_phones()
        if not phones:
            text = "📭 No accounts yet. Use *Add Accounts* to get started."
        else:
            lines = [f"📱 *Accounts ({len(phones)} total):*\n"]
            for i, p in enumerate(phones, 1):
                lines.append(f"`{i}.` {p}")
            text = "\n".join(lines)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="account_manager")]])
        await query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    # ── History view (callback) ────────────────────────────────────────────
    async def _show_history_cb(self, query, context):
        if not os.path.exists(HISTORY_FILE):
            text = "📭 No history yet."
        else:
            with open(HISTORY_FILE) as f:
                history = json.load(f)
            if not history:
                text = "📭 No history yet."
            else:
                lines = ["📋 *Last Operations:*\n"]
                for h in reversed(history[-10:]):
                    lines.append(f"• `{h['ts']}` — *{h['action']}*\n  {h['detail']}")
                text = "\n".join(lines)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="system_tools")]])
        await query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    # ── Logs view ──────────────────────────────────────────────────────────
    async def _show_logs(self, query, context):
        try:
            with open(LOG_FILE, "r") as f:
                lines = f.readlines()
            last = "".join(lines[-20:]).strip() or "No log entries yet."
        except FileNotFoundError:
            last = "Log file not found."
        text = f"📊 *Recent Logs (last 20 lines):*\n\n```\n{last[:3500]}\n```"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="system_tools")]])
        await query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    # ── Stop running operation ─────────────────────────────────────────────
    async def _stop_operation(self, query, context):
        _stop_event.set()
        await query.edit_message_text("🛑 *Stop signal sent.* The operation will halt after the current step.")
        _stop_event.clear()

    # ══════════════════════════════════════════════════════════════════════
    # ADD ACCOUNTS
    # ══════════════════════════════════════════════════════════════════════
    async def _ask_phones(self, query, context):
        await query.edit_message_text(
            "📱 *Add Accounts*\n\n"
            "Send phone numbers like this:\n"
            "```\n3\n+1234567890\n+1234567891\n+1234567892\n```\n"
            "First line = count, then one number per line \\(with country code\\)\\.",
            parse_mode="MarkdownV2"
        )
        context.user_data["expecting_phones"] = True

    async def _process_phones(self, update: Update, text: str):
        lines = text.strip().splitlines()
        try:
            count = int(lines[0])
            numbers = [l.strip() for l in lines[1:count + 1] if l.strip()]
            if len(numbers) != count:
                await update.message.reply_text("❌ Count doesn't match the number of lines provided.")
                return
        except (ValueError, IndexError):
            await update.message.reply_text("❌ Invalid format — first line must be a number.")
            return

        existing = set(read_phones())
        new = [n for n in numbers if n not in existing]
        duplicates = count - len(new)

        if not new:
            await update.message.reply_text("ℹ️ All numbers already exist in phone.csv — nothing added.")
            return

        msg = await update.message.reply_text(f"🔄 Logging in {len(new)} account(s)…\nThis may take a moment.")

        errors = []
        added  = []

        for phone_raw in new:
            if _stop_event.is_set():
                break
            try:
                from pyrogram import Client as PyroClient
                phone = parse_phone(phone_raw)
                app = PyroClient(
                    f"{SESSIONS_DIR}/{phone}",
                    api_id=int(API_ID), api_hash=API_HASH,
                    phone_number=phone
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
                errors.append(f"{phone_raw}: {e}")
                logger.warning(f"Login failed for {phone_raw}: {e}")

        # Save successfully added phones
        all_phones = read_phones() + added
        write_phones(all_phones)

        log_history("Add Accounts", f"Added {len(added)}, {len(errors)} failed, {duplicates} duplicates")

        result = (
            f"✅ *Add Accounts Complete*\n\n"
            f"✔️ Added: `{len(added)}`\n"
            f"⚠️ Failed: `{len(errors)}`\n"
            f"🔁 Duplicates skipped: `{duplicates}`\n"
        )
        if errors:
            result += "\n*Errors:*\n" + "\n".join(f"• {e}" for e in errors[:5])
        result += "\n\nUse /menu to return."
        await msg.edit_text(result, parse_mode="Markdown")

    # ══════════════════════════════════════════════════════════════════════
    # REMOVE BANNED  (runs in background thread, sends updates)
    # ══════════════════════════════════════════════════════════════════════
    async def _run_in_thread(self, query, context, command: str):
        if self._active_task and self._active_task.is_alive():
            await query.edit_message_text("⚠️ Another operation is already running. Use /cancel to stop it first.")
            return

        stop_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🛑 Stop", callback_data="stop_operation")]])
        msg = await query.edit_message_text(
            f"🔄 *Starting {command.replace('_', ' ').title()}…*\nYou'll get live updates here.",
            reply_markup=stop_kb, parse_mode="Markdown"
        )

        chat_id = query.message.chat_id

        async def send_update(text: str):
            try:
                await context.bot.send_message(chat_id, text, parse_mode="Markdown")
            except Exception as e:
                logger.warning(f"Could not send update: {e}")

        loop = asyncio.get_event_loop()

        if command == "remove_banned":
            def task():
                asyncio.run_coroutine_threadsafe(
                    self._do_remove_banned(send_update), loop
                ).result()
        elif command == "check_limits":
            def task():
                asyncio.run_coroutine_threadsafe(
                    self._do_check_limits(send_update), loop
                ).result()
        else:
            return

        self._active_task = threading.Thread(target=task, daemon=True)
        self._active_task.start()

    # ── Remove Banned ──────────────────────────────────────────────────────
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
                    api_id=int(API_ID), api_hash=API_HASH,
                    phone_number=phone
                )
                app.start()
                app.stop()
                active.append(phone_raw)
                logger.info(f"Active: {phone}")
            except (AuthKeyUnregistered, UserDeactivatedBan, SessionExpired, SessionRevoked, UserDeactivated) as e:
                banned.append(phone_raw)
                await send_update(f"⛔ `{phone}` is banned/deactivated — removing.")
                # Delete session file
                session_path = f"{SESSIONS_DIR}/{phone}.session"
                if os.path.exists(session_path):
                    os.remove(session_path)
                logger.info(f"Banned & removed: {phone} ({type(e).__name__})")
            except Exception as e:
                active.append(phone_raw)
                logger.warning(f"Unexpected error for {phone}: {e}")

            if i % 5 == 0:
                await send_update(f"⏳ Progress: `{i}/{len(phones)}` checked…")

        write_phones(active)
        log_history("Remove Banned", f"Removed {len(banned)} banned, {len(active)} active remain")

        await send_update(
            f"✅ *Ban Scan Complete*\n\n"
            f"⛔ Banned & removed: `{len(banned)}`\n"
            f"✔️ Active remaining: `{len(active)}`\n\n"
            f"Use /menu to continue."
        )

    # ── Check & Fix Limits ─────────────────────────────────────────────────
    async def _do_check_limits(self, send_update):
        from pyrogram import Client as PyroClient

        phones = read_phones()
        if not phones:
            await send_update("📭 No accounts in phone.csv.")
            return

        await send_update(f"🔍 Checking limits on `{len(phones)}` account(s) via @SpamBot…")

        url = "https://pastebin.com/raw/YKbeUazQ"
        try:
            import requests as req
            content = req.get(url, timeout=10).text
        except Exception:
            content = "I'm not a spammer."

        results = {"no_limit": [], "limited": [], "fixed": [], "error": []}

        FREE_MSG   = "Good news, no limits"
        HARSH_MSG  = "some phone numbers may trigger"
        LIMITED_MSG = "some actions can trigger a harsh response"

        for i, phone_raw in enumerate(phones, 1):
            if _stop_event.is_set():
                await send_update("🛑 Stopped by user.")
                break

            phone = parse_phone(phone_raw)
            try:
                app = PyroClient(
                    f"{SESSIONS_DIR}/{phone}",
                    api_id=int(API_ID), api_hash=API_HASH,
                    phone_number=phone
                )
                app.start()
                spambot = "spambot"
                app.send_message(spambot, "/start")
                time.sleep(1.5)
                last = next(app.get_chat_history(spambot, limit=1), None)
                if not last:
                    app.stop()
                    results["error"].append(phone)
                    continue

                txt = last.text or ""

                if FREE_MSG in txt:
                    results["no_limit"].append(phone)
                    await send_update(f"✅ `{phone}` — No limit")

                elif HARSH_MSG in txt:
                    app.send_message(spambot, "Submit a complaint")
                    time.sleep(1)
                    r2 = next(app.get_chat_history(spambot, limit=1), None)
                    if r2 and "confirm" in (r2.text or "").lower():
                        app.send_message(spambot, "No, I'll never do any of this!")
                        time.sleep(1)
                        app.send_message(spambot, content)
                        time.sleep(1)
                    results["fixed"].append(phone)
                    await send_update(f"⚠️ `{phone}` — Harsh flag, complaint submitted")

                elif LIMITED_MSG in txt:
                    app.send_message(spambot, "This is a mistake")
                    time.sleep(1)
                    r2 = next(app.get_chat_history(spambot, limit=1), None)
                    if r2 and "complaint" in (r2.text or "").lower():
                        app.send_message(spambot, "Yes")
                        time.sleep(1)
                        app.send_message(spambot, "No! Never did that!")
                        time.sleep(1)
                        app.send_message(spambot, content)
                        time.sleep(1)
                    results["limited"].append(phone)
                    await send_update(f"🔴 `{phone}` — Limited, complaint submitted")

                else:
                    results["error"].append(phone)
                    await send_update(f"❓ `{phone}` — Unknown response from SpamBot")

                app.stop()

            except Exception as e:
                results["error"].append(phone)
                logger.warning(f"Limit check error for {phone}: {e}")

            if i % 3 == 0:
                await send_update(f"⏳ Progress: `{i}/{len(phones)}` checked…")

        log_history(
            "Check Limits",
            f"OK:{len(results['no_limit'])} Fixed:{len(results['fixed'])} "
            f"Limited:{len(results['limited'])} Error:{len(results['error'])}"
        )

        await send_update(
            f"✅ *Limit Check Complete*\n\n"
            f"✔️ No limit: `{len(results['no_limit'])}`\n"
            f"🔧 Fixed/Complaint sent: `{len(results['fixed'])}`\n"
            f"🔴 Still limited: `{len(results['limited'])}`\n"
            f"❓ Errors: `{len(results['error'])}`\n\n"
            f"Use /menu to continue."
        )

    # ══════════════════════════════════════════════════════════════════════
    # GROUP CLONER — ask params
    # ══════════════════════════════════════════════════════════════════════
    async def _ask_gc_params(self, query, context):
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="group_tools")]])
        await query.edit_message_text(
            "📋 *Group Cloner Setup*\n\n"
            "Send parameters — one per line:\n"
            "```\n"
            "source_group\n"
            "target_group\n"
            "message_count\n"
            "delay_seconds\n"
            "start_date (YYYY-MM-DD or leave blank)\n"
            "end_date   (YYYY-MM-DD or leave blank)\n"
            "admin_count (how many of your accounts are admins)\n"
            "```\n"
            "Example:\n"
            "```\n@oldgroup\n@newgroup\n100\n2\n2024-01-01\n2024-12-31\n2\n```",
            reply_markup=kb, parse_mode="Markdown"
        )
        context.user_data["expecting_gc_params"] = True

    async def _ask_realtime_params(self, query, context):
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="group_tools")]])
        await query.edit_message_text(
            "🔄 *Real-time Cloner Setup*\n\n"
            "Send parameters — one per line:\n"
            "```\n"
            "source_group\n"
            "target_group\n"
            "initial_message_count\n"
            "delay_seconds\n"
            "start_date (YYYY-MM-DD or leave blank)\n"
            "end_date   (YYYY-MM-DD or leave blank)\n"
            "admin_count\n"
            "```",
            reply_markup=kb, parse_mode="Markdown"
        )
        context.user_data["expecting_realtime_params"] = True

    def _parse_cloner_params(self, lines: list[str]) -> dict | None:
        if len(lines) < 4:
            return None
        try:
            return {
                "source_group":  lines[0].strip(),
                "target_group":  lines[1].strip(),
                "msg_count":     int(lines[2].strip()),
                "delay":         int(lines[3].strip()),
                "start_date":    lines[4].strip() if len(lines) > 4 else "",
                "end_date":      lines[5].strip() if len(lines) > 5 else "",
                "admin_count":   int(lines[6].strip()) if len(lines) > 6 and lines[6].strip() else 1,
            }
        except (ValueError, IndexError):
            return None

    async def _process_gc_params(self, update: Update, text: str):
        params = self._parse_cloner_params(text.strip().splitlines())
        if not params:
            await update.message.reply_text("❌ Invalid format. Please check the example and try again.")
            return

        phones = read_phones()
        if not phones:
            await update.message.reply_text("❌ No accounts in phone.csv. Add accounts first.")
            return

        msg = await update.message.reply_text(
            f"🔄 *Group Cloner Starting…*\n\n"
            f"Source: `{params['source_group']}`\n"
            f"Target: `{params['target_group']}`\n"
            f"Messages: `{params['msg_count']}`\n"
            f"Delay: `{params['delay']}s`\n\n"
            "_Scraping & sending — live updates to follow…_",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛑 Stop", callback_data="stop_operation")]])
        )
        chat_id = update.message.chat_id
        context = update.get_bot()
        bot = update.get_bot()

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
            await update.message.reply_text("❌ Invalid format. Please check the example and try again.")
            return

        phones = read_phones()
        if not phones:
            await update.message.reply_text("❌ No accounts in phone.csv. Add accounts first.")
            return

        await update.message.reply_text(
            f"🔴 *Real-time Cloner Starting…*\n\n"
            f"Source: `{params['source_group']}`\n"
            f"Target: `{params['target_group']}`\n"
            f"Initial load: `{params['msg_count']}` messages\n"
            f"Delay: `{params['delay']}s`\n\n"
            "_This runs continuously. Use /cancel to stop._",
            parse_mode="Markdown"
        )
        bot = update.get_bot()
        chat_id = update.message.chat_id

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

    # ── Core cloner logic ──────────────────────────────────────────────────
    async def _do_gc_clone(self, send_update, phones: list[str], params: dict, realtime: bool):
        from pyrogram import Client as PyroClient, filters as pyro_filters
        from pyrogram.errors import UserAlreadyParticipant
        from pyrogram.handlers import MessageHandler as PyroMH
        from pyrogram.enums import ChatMembersFilter
        from datetime import datetime as dt

        groupsc   = params["source_group"]
        groupyour = params["target_group"]
        msg_count = params["msg_count"]
        delay     = params["delay"]
        admin_count = max(1, min(params["admin_count"], len(phones)))

        start_ts = None
        end_ts   = None
        if params.get("start_date"):
            try:
                start_ts = int(dt.strptime(params["start_date"], "%Y-%m-%d").timestamp())
            except ValueError:
                await send_update("⚠️ Invalid start_date — ignoring date filter.")
        if params.get("end_date"):
            try:
                end_ts = int(dt.strptime(params["end_date"], "%Y-%m-%d").timestamp())
            except ValueError:
                pass

        # ── Scrape messages & detect admins ────────────────────────────────
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
            await send_update(f"❌ Could not join source group: {e}")
            scout.stop()
            return

        admin_ids = set()
        try:
            for member in scout.get_chat_members(groupsc, filter=ChatMembersFilter.ADMINISTRATORS):
                admin_ids.add(member.user.id)
        except Exception as e:
            await send_update(f"⚠️ Could not fetch admin list: {e}")

        await send_update(f"📡 Scraping `{msg_count}` messages from `{groupsc}`…")

        messages = []
        for m in scout.get_chat_history(groupsc, limit=msg_count):
            ts = m.date.timestamp()
            if start_ts and ts < start_ts:
                continue
            if end_ts and ts > end_ts:
                continue
            messages.append(m)
        messages.reverse()

        message_data = []
        for m in messages:
            is_admin = (not m.from_user) or (m.from_user.id in admin_ids)
            message_data.append((m.id, is_admin))

        scout.stop()
        await send_update(f"✅ Scraped `{len(message_data)}` messages. Joining groups with all accounts…")

        # ── Join groups with all accounts ──────────────────────────────────
        admin_phones   = [parse_phone(phones[i]) for i in range(admin_count)]
        regular_phones = [parse_phone(p) for p in phones[admin_count:]] or admin_phones

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
                try:
                    app.join_chat(groupsc)
                except UserAlreadyParticipant:
                    pass
                try:
                    app.join_chat(groupyour)
                except UserAlreadyParticipant:
                    pass
                app.stop()
            except Exception as e:
                logger.warning(f"Join failed for {phone}: {e}")

        await send_update(
            f"📌 *Make sure these accounts are admins in `{groupyour}` before continuing:*\n"
            + "\n".join(f"• `{p}`" for p in admin_phones)
            + "\n\n_Proceeding in 10 seconds…_"
        )
        time.sleep(10)

        # ── Send messages ──────────────────────────────────────────────────
        await send_update(f"📤 Sending `{len(message_data)}` messages…")
        ai = ri = sent = failed = 0

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
                app = PyroClient(
                    f"{SESSIONS_DIR}/{phone}",
                    api_id=int(API_ID), api_hash=API_HASH, phone_number=phone
                )
                app.start()
                time.sleep(delay)
                app.copy_message(groupyour, groupsc, msg_id)
                app.stop()
                sent += 1
            except Exception as e:
                failed += 1
                logger.warning(f"Copy failed msg {msg_id}: {e}")

            if i % 20 == 0:
                await send_update(f"⏳ Progress: `{i}/{len(message_data)}` — ✔️`{sent}` ❌`{failed}`")

        if not realtime:
            log_history("GC Clone", f"Cloned {sent} msgs {groupsc}→{groupyour}, {failed} failed")
            await send_update(
                f"🎉 *Clone Complete\\!*\n\n"
                f"✔️ Sent: `{sent}`\n❌ Failed: `{failed}`\n\n"
                f"Use /menu to continue\\."
            )
            return

        # ── Real-time monitoring ───────────────────────────────────────────
        await send_update(f"🔴 *Real-time monitoring active on `{groupsc}`*\nNew messages will be auto-forwarded. Use /cancel to stop.")

        last_msg_id  = message_data[-1][0] if message_data else 0
        monitor_phone = parse_phone(phones[0])
        monitor_app = PyroClient(
            f"{SESSIONS_DIR}/{monitor_phone}",
            api_id=int(API_ID), api_hash=API_HASH, phone_number=monitor_phone
        )
        monitor_app.start()
        rt_sent = rt_failed = 0

        def rt_handler(client, message):
            nonlocal last_msg_id, ai, ri, rt_sent, rt_failed
            if message.id <= last_msg_id or _stop_event.is_set():
                return
            last_msg_id = message.id
            is_admin = (not message.from_user) or (message.from_user.id in admin_ids)
            phone = admin_phones[ai % len(admin_phones)] if is_admin else regular_phones[ri % len(regular_phones)]
            if is_admin:
                ai += 1
            else:
                ri += 1
            try:
                fwd = PyroClient(
                    f"{SESSIONS_DIR}/{phone}",
                    api_id=int(API_ID), api_hash=API_HASH, phone_number=phone
                )
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
            log_history("RT Clone", f"Forwarded {rt_sent} real-time msgs {groupsc}→{groupyour}, {rt_failed} failed")
            asyncio.run_coroutine_threadsafe(
                send_update(
                    f"🛑 *Real-time monitoring stopped*\n\n"
                    f"✔️ Forwarded: `{rt_sent}`\n❌ Failed: `{rt_failed}`"
                ), asyncio.get_event_loop()
            )

    # ══════════════════════════════════════════════════════════════════════
    # Message router (text inputs during multi-step flows)
    # ══════════════════════════════════════════════════════════════════════
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
        else:
            await update.message.reply_text(
                "ℹ️ No operation active. Use /menu to access controls.",
                parse_mode="Markdown"
            )

    # ── Run ────────────────────────────────────────────────────────────────
    def run(self):
        logger.info("🚀 TGTX Bot starting…")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise SystemExit("❌ BOT_TOKEN not set. Set the BOT_TOKEN environment variable.")
    TGTXBot(BOT_TOKEN).run()


if __name__ == "__main__":
    main()
