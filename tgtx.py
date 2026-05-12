import os
import base64
import hashlib
import uuid
from cryptography.fernet import Fernet

LICENSE_FILE = "license.key"

# Encryption key (must be the same as in setup.py)
SECRET_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"my_secret_phrase").digest()[:32])

# Pre-approved activation keys
VALID_KEYS = [
    "A9D7KLMXRT52QWECNJ8VZ3HUB"  # First Mac PC
]

def get_hardware_id():
    """Gets the current PC's unique hardware ID."""
    return hashlib.sha256(uuid.getnode().to_bytes(6, 'big')).hexdigest()

def decrypt_data(data):
    """Decrypts the activation key stored in license.key."""
    cipher = Fernet(SECRET_KEY)
    return cipher.decrypt(data.encode()).decode()

def validate_activation():
    """Ensures the activation key is valid before running the app."""
    if not os.path.exists(LICENSE_FILE):
        print("❌ No activation key found. Please run setup.py first.")
        exit()

    try:
        with open(LICENSE_FILE, "r") as f:
            stored_data = decrypt_data(f.read().strip())  # Decrypt stored key
        
        activation_key, registered_hardware = stored_data.split(":")  # Extract key and hardware ID
        
        if activation_key not in VALID_KEYS:
            print("❌ Invalid or tampered license key detected!")
            exit()
        
        if registered_hardware != get_hardware_id():
            print("❌ This license is registered to another computer!")
            exit()

        print("✅ Activation verified! Running application...")
    except Exception as e:
        print("❌ License key is corrupt or modified!", e)
        exit()

validate_activation()  # Run activation check first

print("🎉 Running TGTX application...")



import sys
import pickle, os
from time import sleep
import webbrowser
import time
import random
import string
import pyfiglet
from pyrogram import Client
import asyncio
from pyrogram.errors import FloodWait
from pyrogram.errors import PeerFlood
from pyrogram.errors import PeerIdInvalid
from pyrogram.errors import UserNotParticipant
from pyrogram.errors import UserNotMutualContact
from pyrogram.errors import UserPrivacyRestricted
from pyrogram.errors import UserNotParticipant, UserAlreadyParticipant
from pyrogram.errors import UserChannelsTooMuch
from pyrogram.errors import UserIdInvalid
from pyrogram.errors import UserKicked
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors import UserBannedInChannel
from pyrogram.errors import RPCError
from pyrogram.errors import PhoneNumberUnoccupied
from pyrogram.errors import PhoneNumberInvalid
from pyrogram.errors import PhoneNumberOccupied
from pyrogram.errors import PhoneNumberBanned
from pyrogram.errors import PhoneNumberFlood
from pyrogram.errors import ApiIdInvalid
import datetime
import gender_guesser.detector as gender
from pyrogram import types
from pyrogram.raw import functions, types
from pyrogram.enums import UserStatus
from pyrogram.errors import UserDeactivated, AuthKeyUnregistered, SessionExpired, UserDeactivatedBan, SessionRevoked
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import ChatEventFilter, InputPhoneContact
import time
import configparser
import csv
from csv import reader
from colorama import Fore, Back, Style, init
import colorama
colorama.init(autoreset=True)
from telethon import utils
import traceback
from licensing.models import *
from licensing.methods import Key, Helpers
import requests
from geopy.geocoders import Nominatim
from ts import messagesendergroup, messagesendergrouppic, messagesendergrouppicsingle, messagesendergroupsingle, messagesendergroupmultimsg, messagesendergroupmultimsgpic, messagesendergroupmultimsgpicmultigroups, messagesendergroupmultimsgmultigroups, messagesendermultigroupsinglepic, messagesendermultigroupsingle, forward_to_channels, forward_to_channelsnotag, multi_ccraper, messagesendering, messagesenderingpic, addtocontactbyimp, addtocontactbygroup
from faker import Faker
import os
import time
import csv
import random
from datetime import datetime, timedelta
from pyrogram import Client, errors
scam = '@notoscam'
init()

if not os.path.exists('./sessions'):
    os.mkdir('./sessions')

api_id = '23269382'
api_hash = "fe19c565fb4378bd5128885428ff8e26"

r = Fore.RED
n = Fore.RESET
lg = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
grey = '\033[97m'
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]
info = lg + '[' + w + 'i' + lg + ']' + rs
error = lg + '[' + r + '!' + lg + ']' + rs
success = w + '[' + lg + '*' + w + ']' + rs
INPUT = lg + '[' + cy + '~' + lg + ']' + rs
plus = w + '[' + lg + '+' + w + ']' + rs
minus = w + '[' + lg + '-' + w + ']' + rs
re="\033[1;31m"
gr="\033[1;32m"
wi="\033[1;35m"

try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing module - requests...{n}')
    os.system('pip install requests')

def banner():
    import random
    
    b= [
'████████╗░██████╗░██╗░░██╗████████╗',
'╚══██╔══╝██╔════╝░╚██╗██╔╝╚══██╔══╝',
'░░░██║░░░██║░░██╗░░╚███╔╝░░░░██║░░░',
'░░░██║░░░██║░░╚██╗░██╔██╗░░░░██║░░░',
'░░░██║░░░╚██████╔╝██╔╝╚██╗░░░██║░░░',
'░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░',
    ]
    for char in b:
        print(f'{char}{w}')
    print(f'{gr}Made by BabzTech{re}')
    print(f'{re}Developer : BabzTech{r}')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def login():

    if not os.path.exists(f'phone.csv'):
        fp = open('phone.csv', 'x')
        fp.close()
    with open('phone.csv', mode='a', newline='') as file:
         writer = csv.writer(file)
         writer.writerow([])
         
    def remove_blank_lines(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        with open(filename, 'w') as f:
            f.writelines(line for line in lines if line.strip())

    def remove_duplicates(lst):
        return list(set(lst))
    print()
    num_accounts = int(input(f"{gr}Enter the number of accounts you want to add:{w} "))
    
    phone_numbers = []
    print()
    for i in range(num_accounts):
        phone = input(f"{gr}Enter phone number for account {i + 1}:{re} ")
        phone_numbers.append(phone)

    remove_blank_lines('phone.csv')
    with open('phone.csv', 'r') as f:
        str_lists = [row[0] for row in csv.reader(f)]
        
    phone_numbers = remove_duplicates(phone_numbers)
    
    with open('phone.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for phone in phone_numbers:
            if phone not in str_lists:
                phones = utils.parse_phone(phone)
                print(Style.BRIGHT + Fore.GREEN + f"Login {phones}")
                app = Client(f'sessions/{phones}', api_id, api_hash,phone_number=phones)
                app.start()
                app.join_chat('@The_Hacking_Zone')
                time.sleep(4.0)
                app.join_chat('@Techno_Trickop')
                app.stop()
                writer.writerow([phone])
    print()
    print(Style.BRIGHT + Fore.RESET + 'All Number Login Done !')
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to Exit')
    input()


def specificaccremove():

    if not os.path.exists(f'phone.csv'):
        fp = open('phone.csv', 'x')
        fp.close()
        
    def remove_blank_lines(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        with open(filename, 'w') as f:
            f.writelines(line for line in lines if line.strip())

    def remove_duplicates(lst):
        return list(set(lst))

    def display_phone_numbers():
        with open('phone.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            phone_numbers = [row[0] for row in reader]
            for i, phone in enumerate(phone_numbers, start=1):
                print(f"{gr}{i}. {phone}")

    remove_blank_lines('phone.csv')
    print()
    print(f"{re}All Phone Numbers:")
    display_phone_numbers()
    print()
    to_remove = input(f"{Style.BRIGHT + ye}Enter the numbers of the accounts to remove (comma-separated):{re} ").split(',')
    to_remove = [int(num) for num in to_remove]

    with open('phone.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        phone_numbers = [row[0] for row in reader]

    removed_accounts = []
    for i in sorted(to_remove, reverse=True):  # Iterate in reverse to avoid index issues
        if i >= 1 and i <= len(phone_numbers):
           removed_accounts.append(phone_numbers.pop(i - 1))

    with open('phone.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for phone in phone_numbers:
            writer.writerow([phone])
    print()
    print(f"{re}Removed Accounts:")
    for account in removed_accounts:
        print(f"{gr}{account}")

    print(Style.BRIGHT + Fore.RESET + 'Accounts Removed!')
    print()
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to exit')
    input()

def BanFilter():

    if not os.path.exists(f'BanNumbers.csv'):
        fp = open('BanNumbers.csv', 'x')
        fp.close()
        
    MadeByHackingZone = []

    done = False
    with open('phone.csv', 'r') as f:
        str_list = [row[0] for row in csv.reader(f)]

        po = 0
        for unparsed_phone in str_list:
            po += 1

            phone = utils.parse_phone(unparsed_phone)

            print(f"{gr}Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            # client.start(phone)
            try:
                    app.start()
                    continue

            except AuthKeyUnregistered:
                    print(f'{re}Maybe you or someone Terminated this Session')
                    HackingZone = str(po)
                    Nero_op = str(unparsed_phone)
                    MadeByHackingZone.append(Nero_op)
                    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
                         writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")
                         writer.writerows(MadeByHackingZone)

            except UserDeactivatedBan:
                    print(f'{re}This account is banned')
                    HackingZone = str(po)
                    Nero_op = str(unparsed_phone)
                    MadeByHackingZone.append(Nero_op)
                    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
                         writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

                         writer.writerows(MadeByHackingZone)
                         
            except SessionExpired:
                    print(f'{re}This Session was Expired')
                    HackingZone = str(po)
                    Nero_op = str(unparsed_phone)
                    MadeByHackingZone.append(Nero_op)
                    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
                         writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

                         writer.writerows(MadeByHackingZone)
                         
            except SessionRevoked:
                    print(f'{re}The authorization has been invalidated, because of the user terminating all sessions')
                    HackingZone = str(po)
                    Nero_op = str(unparsed_phone)
                    MadeByHackingZone.append(Nero_op)
                    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
                         writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

                         writer.writerows(MadeByHackingZone)
                         
            except UserDeactivated:
                    print(f'{re} Account User Deactivated or Account Banned')
                    HackingZone = str(po)
                    Nero_op = str(unparsed_phone)
                    MadeByHackingZone.append(Nero_op)
                    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
                         writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

                         writer.writerows(MadeByHackingZone)

                    continue

            # client.disconnect()
        done = True
        print(f'{gr}List Of Banned Numbers')
        print(*MadeByHackingZone, sep='\n')
        print(f'{gr}Saved In BanNumbers.csv')


    def autoremove():


        collection = []
        nc = []
        collection1 = []
        nc1 = []
        maind = []

        with open("phone.csv", "r") as infile:
            for line in infile:
                collection.append(line)

        for x in collection:
            mod_x = str(x).replace("\n", "")
            nc.append(mod_x)

        with open("BanNumbers.csv") as infile, open("outfile.csv", "w") as outfile:
            for line in infile:
                outfile.write(line.replace(",", ""))

        with open("outfile.csv", "r") as outfile:
            for line1 in outfile:
                rrr = line1.replace("\n", "")
                os.remove(f'sessions/{rrr}.session')
                collection1.append(line1)

        for i in collection1:
            mod_i = str(i).replace("\n", "")
            nc1.append(mod_i)

        unique = set(nc)
        unique1 = set(nc1)

        itd = unique.intersection(unique1)

        for x in nc:
            if x not in itd:
                maind.append(x)

        with open('unban.csv', 'w', encoding='UTF-8') as writeFile:
            writer = csv.writer(writeFile, lineterminator="\n")
            writer.writerows(maind)

        with open("unban.csv") as last, open("phone.csv", "w") as final:
            for line3 in last:
                mod_i = str(line3).replace("\n", "")
                final.write(mod_i)

        os.remove("phone.csv")
        os.rename("unban.csv", "phone.csv")
        print("Done,All Banned Number Have Been Removed")


    def dellst():
        import csv
        import os

        with open("phone.csv") as infile, open("unban.csv", "w") as outfile:
            for line in infile:
                outfile.write(line.replace(",", ""))

        os.remove("phone.csv")
        os.rename("unban.csv", "phone.csv")

        print("complete")


    autoremove()
    dellst()

    input("Done!" if done else "Error!")

def groupchatcloner_with_admin():
    if os.path.exists('scrmessage.csv'):
        os.remove('scrmessage.csv')
    open('scrmessage.csv', 'x').close()
    
    groupsc = str(input(f"{gr}Enter Target Group Username or Private Link: {re}"))
    groupyour = str(input(f"{gr}Enter Your Group Link: {re}"))
    groupmsg = int(input(f"{gr}Enter Number of messages to scrape: {re}"))
    delayper = int(input(f"{gr}Enter Delay Per Second between per Message: {re}"))

    # Get start and end date from user
    start_date_str = input(f"{gr}Enter start date (YYYY-MM-DD) or leave blank for all messages: {re}").strip()
    end_date_str = input(f"{gr}Enter end date (YYYY-MM-DD) or leave blank to scrape until the latest message: {re}").strip()

    start_timestamp = None
    end_timestamp = None

    # Convert dates to timestamps
    if start_date_str:
        try:
            start_timestamp = int(datetime.strptime(start_date_str, "%Y-%m-%d").timestamp())
        except ValueError:
            print(f"{re}Invalid start date format! Please enter in YYYY-MM-DD format.")
            return

    if end_date_str:
        try:
            end_timestamp = int(datetime.strptime(end_date_str, "%Y-%m-%d").timestamp())
        except ValueError:
            print(f"{re}Invalid end date format! Please enter in YYYY-MM-DD format.")
            return

    # Store message IDs with admin flag and preview
    def save_messages(message_id, is_admin, preview):
        with open('scrmessage.csv', 'a', encoding='utf-8') as file:
            # Escape commas and newlines in preview
            preview_escaped = preview.replace(',', '|||').replace('\n', ' ').replace('\r', ' ')
            file.write(f"{message_id},{is_admin},{preview_escaped}\n")

    # Scrape messages and detect admin status
    with open('phone.csv', 'r') as f:
        first_number = f.readline().strip()
        pphone = first_number
        if pphone:
            phone = utils.parse_phone(pphone)
            print(Style.BRIGHT + Fore.GREEN + f"Getting messages from {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone)
            app.start()
            
            try:
                app.join_chat(groupsc)
            except UserAlreadyParticipant:
                pass
            
            try:
                sc_entity = app.get_chat(groupsc)
            except Exception as e:
                print(e)
                app.stop()
                return

            # Get list of admins in source group
            admin_ids = []
            admin_names = {}
            try:
                from pyrogram.enums import ChatMembersFilter
                for member in app.get_chat_members(sc_entity.id, filter=ChatMembersFilter.ADMINISTRATORS):
                    admin_ids.append(member.user.id)
                    admin_names[member.user.id] = member.user.first_name
                    print(f"{gr}Detected admin: {member.user.first_name} (ID: {member.user.id}){re}")
            except Exception as e:
                print(f"{ye}Warning: Could not fetch admin list: {e}")
                print(f"{ye}Attempting alternative method...{re}")
                try:
                    chat = app.get_chat(sc_entity.id)
                    admins = app.get_chat_members(sc_entity.id, limit=200, filter=ChatMembersFilter.ADMINISTRATORS)
                    for admin in admins:
                        admin_ids.append(admin.user.id)
                        admin_names[admin.user.id] = admin.user.first_name
                        print(f"{gr}Detected admin: {admin.user.first_name} (ID: {admin.user.id}){re}")
                except Exception as e2:
                    print(f"{re}Could not detect admins. All messages will be sent as regular messages.{re}")
                    print(f"{re}Error: {e2}{re}")

            # Fetch messages within date range
            messages = []
            for message in app.get_chat_history(sc_entity.id, limit=groupmsg):
                message_timestamp = message.date.timestamp()

                if (start_timestamp and message_timestamp < start_timestamp) or \
                   (end_timestamp and message_timestamp > end_timestamp):
                    continue

                messages.append(message)

            messages.reverse()

            # Display message preview and save
            print(f"\n{cy}{'='*80}{re}")
            print(f"{cy}MESSAGE PREVIEW - Showing sender type for each message{re}")
            print(f"{cy}{'='*80}{re}\n")
            
            admin_count = 0
            regular_count = 0
            unknown_count = 0
            
            for message in messages:
                # Check if sender is known admin OR if sender is Unknown (treat as admin)
                is_known_admin = message.from_user and message.from_user.id in admin_ids
                is_unknown_sender = not message.from_user
                is_admin = is_known_admin or is_unknown_sender
                
                # Get message preview
                if message.text:
                    preview_text = message.text.replace('\n', ' ').replace('\r', ' ')
                    preview = preview_text[:50] + "..." if len(preview_text) > 50 else preview_text
                elif message.caption:
                    caption_text = message.caption.replace('\n', ' ').replace('\r', ' ')
                    preview = f"[Media] {caption_text[:40]}..." if len(caption_text) > 40 else f"[Media] {caption_text}"
                elif message.photo:
                    preview = "[Photo]"
                elif message.video:
                    preview = "[Video]"
                elif message.document:
                    preview = "[Document]"
                elif message.sticker:
                    preview = "[Sticker]"
                else:
                    preview = "[Other Media]"
                
                sender_name = "Unknown"
                if message.from_user:
                    sender_name = message.from_user.first_name
                
                if is_admin:
                    admin_count += 1
                    if is_unknown_sender:
                        unknown_count += 1
                        print(f"{ye}👑 ADMIN (Bot/Unknown) [{message.id}] {sender_name}: {preview}{re}")
                    else:
                        print(f"{ye}👑 ADMIN [{message.id}] {sender_name}: {preview}{re}")
                else:
                    regular_count += 1
                    print(f"{gr}👤 Member [{message.id}] {sender_name}: {preview}{re}")
                
                save_messages(message.id, is_admin, preview)

            app.stop()
            print(f"\n{cy}{'='*80}{re}")
            print(f"{gr}Messages scraped successfully!{re}")
            print(f"{gr}📊 Found {len(admin_ids)} known admin(s), {unknown_count} unknown/bot messages (treated as admin){re}")
            print(f"{gr}📊 Total: {admin_count} admin messages, {regular_count} regular messages{re}\n")

    # Select admin accounts for your new group
    print(f"\n{cy}{'='*60}{re}")
    print(f"{cy}SELECT ADMIN ACCOUNTS FOR YOUR NEW GROUP{re}")
    print(f"{cy}{'='*60}{re}\n")
    
    with open('phone.csv', 'r') as f:
        phone_numbers = [row[0] for row in csv.reader(f)]
        print(f"{gr}Available accounts:{re}")
        for idx, phone in enumerate(phone_numbers, 1):
            print(f"{gr}[{idx}] {phone}{re}")
    
    print(f"\n{ye}How many accounts should be admins in your new group?{re}")
    num_admins = int(input(f"{gr}Enter number (1-{len(phone_numbers)}): {re}"))
    
    admin_phones = []
    for i in range(num_admins):
        choice = int(input(f"{gr}Enter account number for admin #{i+1}: {re}")) - 1
        admin_phones.append(utils.parse_phone(phone_numbers[choice]))
    
    print(f"\n{gr}Selected {num_admins} admin account(s):{re}")
    for ap in admin_phones:
        print(f"{ye}  👑 {ap}{re}")

    # Join groups with all accounts
    print(f"\n{cy}Joining groups...{re}")
    with open('phone.csv', 'r') as f:
        phone_numbers = [row[0] for row in csv.reader(f)]
        for pphone in phone_numbers:
            phone = utils.parse_phone(pphone)
            print(Style.BRIGHT + Fore.GREEN + f"Joining with {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone)
            try:
                app.start()
                app.join_chat(groupsc)
                time.sleep(2)
                app.join_chat(groupyour)
                print(f'{wi}Join Successful')
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                print(e)
            app.stop()

    # Remind user to set admins
    print(f"\n{ye}⚠️  IMPORTANT: Make sure these accounts are ADMINS in {groupyour}:{re}")
    for ap in admin_phones:
        print(f"{ye}  👑 {ap}{re}")
    input(f"{gr}Press Enter when you've made them admins...{re}")

    # Read scraped messages with admin flags
    message_data = []
    with open('scrmessage.csv', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',', 2)  # Split on first 2 commas only
            message_id = int(parts[0])
            is_admin = parts[1] == 'True'
            message_data.append((message_id, is_admin))

    # Separate admin and regular accounts
    regular_accounts = [p for p in phone_numbers if utils.parse_phone(p) not in admin_phones]
    
    if len(regular_accounts) == 0:
        print(f"{ye}Warning: All accounts are admins. Using admins for regular messages too.{re}")
        regular_accounts = phone_numbers

    # Send messages with proper account selection
    print(f"\n{cy}{'='*60}{re}")
    print(f"{cy}SENDING MESSAGES{re}")
    print(f"{cy}{'='*60}{re}\n")
    
    admin_index = 0
    regular_index = 0
    admin_msg_count = 0
    regular_msg_count = 0

    for message_id, is_admin in message_data:
        if is_admin:
            # Rotate through admin accounts for admin messages
            phone = admin_phones[admin_index % len(admin_phones)]
            admin_index += 1
            account_type = "👑 ADMIN"
            admin_msg_count += 1
        else:
            # Rotate through regular accounts for non-admin messages
            phone = utils.parse_phone(regular_accounts[regular_index % len(regular_accounts)])
            regular_index += 1
            account_type = "👤 Member"
            regular_msg_count += 1

        print(Style.BRIGHT + Fore.CYAN + f"{account_type} Using {phone}")
        
        app = Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone)
        app.start()
        time.sleep(delayper)

        try:
            app.copy_message(groupyour, groupsc, message_id)
            print(f"{gr}✓ Message {message_id} copied successfully by {account_type}!{re}")
        except Exception as e:
            print(f"{re}✗ Failed to copy message {message_id}: {e}")

        app.stop()

    print(f"\n{cy}{'='*60}{re}")
    print(f"{gr}🎉 All messages sent successfully!{re}")
    print(f"{gr}📊 Admin messages ({admin_msg_count}) distributed across {len(admin_phones)} admin(s){re}")
    print(f"{gr}📊 Regular messages ({regular_msg_count}) distributed across {len(regular_accounts)} account(s){re}")
    print(f"{cy}{'='*60}{re}\n")

def groupchatcloner_realtime():
    """Real-time group chat cloner that monitors and auto-forwards new messages"""
    
    if os.path.exists('scrmessage.csv'):
        os.remove('scrmessage.csv')
    open('scrmessage.csv', 'x').close()
    
    groupsc = str(input(f"{gr}Enter Target Group Username or Private Link: {re}"))
    groupyour = str(input(f"{gr}Enter Your Group Link: {re}"))
    groupmsg = int(input(f"{gr}Enter Number of initial messages to scrape: {re}"))
    delayper = int(input(f"{gr}Enter Delay Per Second between per Message: {re}"))

    # Get start and end date from user
    start_date_str = input(f"{gr}Enter start date (YYYY-MM-DD) or leave blank for all messages: {re}").strip()
    end_date_str = input(f"{gr}Enter end date (YYYY-MM-DD) or leave blank to scrape until the latest message: {re}").strip()

    start_timestamp = None
    end_timestamp = None

    # Convert dates to timestamps
    if start_date_str:
        try:
            start_timestamp = int(datetime.strptime(start_date_str, "%Y-%m-%d").timestamp())
        except ValueError:
            print(f"{re}Invalid start date format! Please enter in YYYY-MM-DD format.")
            return

    if end_date_str:
        try:
            end_timestamp = int(datetime.strptime(end_date_str, "%Y-%m-%d").timestamp())
        except ValueError:
            print(f"{re}Invalid end date format! Please enter in YYYY-MM-DD format.")
            return

    # Store message IDs with admin flag and preview
    def save_messages(message_id, is_admin, preview):
        with open('scrmessage.csv', 'a', encoding='utf-8') as file:
            preview_escaped = preview.replace(',', '|||').replace('\n', ' ').replace('\r', ' ')
            file.write(f"{message_id},{is_admin},{preview_escaped}\n")

    # Scrape initial messages and detect admin status
    with open('phone.csv', 'r') as f:
        first_number = f.readline().strip()
        pphone = first_number
        if pphone:
            phone = utils.parse_phone(pphone)
            print(Style.BRIGHT + Fore.GREEN + f"Getting messages from {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone)
            app.start()
            
            try:
                app.join_chat(groupsc)
            except UserAlreadyParticipant:
                pass
            
            try:
                sc_entity = app.get_chat(groupsc)
            except Exception as e:
                print(e)
                app.stop()
                return

            # Get list of admins in source group
            admin_ids = []
            admin_names = {}
            try:
                from pyrogram.enums import ChatMembersFilter
                for member in app.get_chat_members(sc_entity.id, filter=ChatMembersFilter.ADMINISTRATORS):
                    admin_ids.append(member.user.id)
                    admin_names[member.user.id] = member.user.first_name
                    print(f"{gr}Detected admin: {member.user.first_name} (ID: {member.user.id}){re}")
            except Exception as e:
                print(f"{ye}Warning: Could not fetch admin list: {e}")
                print(f"{ye}Attempting alternative method...{re}")
                try:
                    chat = app.get_chat(sc_entity.id)
                    admins = app.get_chat_members(sc_entity.id, limit=200, filter=ChatMembersFilter.ADMINISTRATORS)
                    for admin in admins:
                        admin_ids.append(admin.user.id)
                        admin_names[admin.user.id] = admin.user.first_name
                        print(f"{gr}Detected admin: {admin.user.first_name} (ID: {admin.user.id}){re}")
                except Exception as e2:
                    print(f"{re}Could not detect admins. All messages will be sent as regular messages.{re}")
                    print(f"{re}Error: {e2}{re}")

            # Fetch initial messages within date range
            messages = []
            for message in app.get_chat_history(sc_entity.id, limit=groupmsg):
                message_timestamp = message.date.timestamp()

                if (start_timestamp and message_timestamp < start_timestamp) or \
                   (end_timestamp and message_timestamp > end_timestamp):
                    continue

                messages.append(message)

            messages.reverse()

            # Display message preview and save
            print(f"\n{cy}{'='*80}{re}")
            print(f"{cy}MESSAGE PREVIEW - Showing sender type for each message{re}")
            print(f"{cy}{'='*80}{re}\n")
            
            admin_count = 0
            regular_count = 0
            unknown_count = 0
            
            for message in messages:
                is_known_admin = message.from_user and message.from_user.id in admin_ids
                is_unknown_sender = not message.from_user
                is_admin = is_known_admin or is_unknown_sender
                
                # Get message preview
                if message.text:
                    preview_text = message.text.replace('\n', ' ').replace('\r', ' ')
                    preview = preview_text[:50] + "..." if len(preview_text) > 50 else preview_text
                elif message.caption:
                    caption_text = message.caption.replace('\n', ' ').replace('\r', ' ')
                    preview = f"[Media] {caption_text[:40]}..." if len(caption_text) > 40 else f"[Media] {caption_text}"
                elif message.photo:
                    preview = "[Photo]"
                elif message.video:
                    preview = "[Video]"
                elif message.document:
                    preview = "[Document]"
                elif message.sticker:
                    preview = "[Sticker]"
                else:
                    preview = "[Other Media]"
                
                sender_name = "Unknown"
                if message.from_user:
                    sender_name = message.from_user.first_name
                
                if is_admin:
                    admin_count += 1
                    if is_unknown_sender:
                        unknown_count += 1
                        print(f"{ye}👑 ADMIN (Bot/Unknown) [{message.id}] {sender_name}: {preview}{re}")
                    else:
                        print(f"{ye}👑 ADMIN [{message.id}] {sender_name}: {preview}{re}")
                else:
                    regular_count += 1
                    print(f"{gr}👤 Member [{message.id}] {sender_name}: {preview}{re}")
                
                save_messages(message.id, is_admin, preview)

            app.stop()
            print(f"\n{cy}{'='*80}{re}")
            print(f"{gr}Messages scraped successfully!{re}")
            print(f"{gr}📊 Found {len(admin_ids)} known admin(s), {unknown_count} unknown/bot messages (treated as admin){re}")
            print(f"{gr}📊 Total: {admin_count} admin messages, {regular_count} regular messages{re}\n")

    # Select admin accounts for your new group
    print(f"\n{cy}{'='*60}{re}")
    print(f"{cy}SELECT ADMIN ACCOUNTS FOR YOUR NEW GROUP{re}")
    print(f"{cy}{'='*60}{re}\n")
    
    with open('phone.csv', 'r') as f:
        phone_numbers = [row[0] for row in csv.reader(f)]
        print(f"{gr}Available accounts:{re}")
        for idx, phone in enumerate(phone_numbers, 1):
            print(f"{gr}[{idx}] {phone}{re}")
    
    print(f"\n{ye}How many accounts should be admins in your new group?{re}")
    num_admins = int(input(f"{gr}Enter number (1-{len(phone_numbers)}): {re}"))
    
    admin_phones = []
    for i in range(num_admins):
        choice = int(input(f"{gr}Enter account number for admin #{i+1}: {re}")) - 1
        admin_phones.append(utils.parse_phone(phone_numbers[choice]))
    
    print(f"\n{gr}Selected {num_admins} admin account(s):{re}")
    for ap in admin_phones:
        print(f"{ye}  👑 {ap}{re}")

    # Join groups with all accounts
    print(f"\n{cy}Joining groups...{re}")
    with open('phone.csv', 'r') as f:
        phone_numbers = [row[0] for row in csv.reader(f)]
        for pphone in phone_numbers:
            phone = utils.parse_phone(pphone)
            print(Style.BRIGHT + Fore.GREEN + f"Joining with {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone)
            try:
                app.start()
                app.join_chat(groupsc)
                time.sleep(2)
                app.join_chat(groupyour)
                print(f'{wi}Join Successful')
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                print(e)
            app.stop()

    # Remind user to set admins
    print(f"\n{ye}⚠️  IMPORTANT: Make sure these accounts are ADMINS in {groupyour}:{re}")
    for ap in admin_phones:
        print(f"{ye}  👑 {ap}{re}")
    input(f"{gr}Press Enter when you've made them admins...{re}")

    # Read scraped messages with admin flags
    message_data = []
    with open('scrmessage.csv', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',', 2)
            message_id = int(parts[0])
            is_admin = parts[1] == 'True'
            message_data.append((message_id, is_admin))

    # Separate admin and regular accounts
    regular_accounts = [p for p in phone_numbers if utils.parse_phone(p) not in admin_phones]
    
    if len(regular_accounts) == 0:
        print(f"{ye}Warning: All accounts are admins. Using admins for regular messages too.{re}")
        regular_accounts = phone_numbers

    # Send initial messages
    print(f"\n{cy}{'='*60}{re}")
    print(f"{cy}SENDING INITIAL MESSAGES{re}")
    print(f"{cy}{'='*60}{re}\n")
    
    admin_index = 0
    regular_index = 0
    admin_msg_count = 0
    regular_msg_count = 0

    for message_id, is_admin in message_data:
        if is_admin:
            phone = admin_phones[admin_index % len(admin_phones)]
            admin_index += 1
            account_type = "👑 ADMIN"
            admin_msg_count += 1
        else:
            phone = utils.parse_phone(regular_accounts[regular_index % len(regular_accounts)])
            regular_index += 1
            account_type = "👤 Member"
            regular_msg_count += 1

        print(Style.BRIGHT + Fore.CYAN + f"{account_type} Using {phone}")
        
        app = Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone)
        app.start()
        time.sleep(delayper)

        try:
            app.copy_message(groupyour, groupsc, message_id)
            print(f"{gr}✓ Message {message_id} copied successfully by {account_type}!{re}")
        except Exception as e:
            print(f"{re}✗ Failed to copy message {message_id}: {e}")

        app.stop()

    print(f"\n{cy}{'='*60}{re}")
    print(f"{gr}🎉 Initial messages sent successfully!{re}")
    print(f"{gr}📊 Admin messages ({admin_msg_count}) distributed across {len(admin_phones)} admin(s){re}")
    print(f"{gr}📊 Regular messages ({regular_msg_count}) distributed across {len(regular_accounts)} account(s){re}")
    print(f"{cy}{'='*60}{re}\n")

    # Now start real-time monitoring
    print(f"\n{cy}{'='*60}{re}")
    print(f"{cy}🔴 STARTING REAL-TIME MONITORING{re}")
    print(f"{cy}{'='*60}{re}\n")
    print(f"{gr}Monitoring {groupsc} for new messages...{re}")
    print(f"{ye}Press Ctrl+C to stop monitoring{re}\n")

    # Use the first account for monitoring
    monitor_phone = utils.parse_phone(phone_numbers[0])
    monitor_app = Client(f'sessions/{monitor_phone}', api_id, api_hash, phone_number=monitor_phone)
    monitor_app.start()

    # Get the last message ID to track new messages
    last_message_id = message_data[-1][0] if message_data else 0

    from pyrogram import filters
    from pyrogram.handlers import MessageHandler

    # Track indices for rotation
    monitoring_admin_index = 0
    monitoring_regular_index = 0
    realtime_admin_count = 0
    realtime_regular_count = 0

    def new_message_handler(client, message):
        nonlocal monitoring_admin_index, monitoring_regular_index, last_message_id
        nonlocal realtime_admin_count, realtime_regular_count
        
        # Only process messages newer than the last scraped message
        if message.id <= last_message_id:
            return
        
        # Update last message ID
        last_message_id = message.id
        
        # Determine if sender is admin or unknown (bot)
        is_known_admin = message.from_user and message.from_user.id in admin_ids
        is_unknown_sender = not message.from_user
        is_admin = is_known_admin or is_unknown_sender
        
        # Get sender name for logging
        sender_name = "Unknown"
        if message.from_user:
            sender_name = message.from_user.first_name
        
        # Get message preview
        if message.text:
            preview_text = message.text.replace('\n', ' ').replace('\r', ' ')
            preview = preview_text[:50] + "..." if len(preview_text) > 50 else preview_text
        elif message.caption:
            caption_text = message.caption.replace('\n', ' ').replace('\r', ' ')
            preview = f"[Media] {caption_text[:40]}..." if len(caption_text) > 40 else f"[Media] {caption_text}"
        elif message.photo:
            preview = "[Photo]"
        elif message.video:
            preview = "[Video]"
        elif message.document:
            preview = "[Document]"
        elif message.sticker:
            preview = "[Sticker]"
        else:
            preview = "[Other Media]"
        
        # Select appropriate account
        if is_admin:
            phone = admin_phones[monitoring_admin_index % len(admin_phones)]
            monitoring_admin_index += 1
            account_type = "👑 ADMIN"
            realtime_admin_count += 1
            
            if is_unknown_sender:
                print(f"\n{ye}🔴 NEW ADMIN MESSAGE (Bot/Unknown) [{message.id}]{re}")
            else:
                print(f"\n{ye}🔴 NEW ADMIN MESSAGE from {sender_name} [{message.id}]{re}")
        else:
            phone = utils.parse_phone(regular_accounts[monitoring_regular_index % len(regular_accounts)])
            monitoring_regular_index += 1
            account_type = "👤 Member"
            realtime_regular_count += 1
            print(f"\n{gr}🔴 NEW MEMBER MESSAGE from {sender_name} [{message.id}]{re}")
        
        print(f"{cy}Preview: {preview}{re}")
        print(f"{cy}Forwarding with {account_type} account: {phone}{re}")
        
        # Forward the message using appropriate account
        forward_app = Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone)
        forward_app.start()
        time.sleep(delayper)
        
        try:
            forward_app.copy_message(groupyour, groupsc, message.id)
            print(f"{gr}✓ Message forwarded successfully!{re}")
            print(f"{cy}📊 Real-time stats: {realtime_admin_count} admin msgs, {realtime_regular_count} regular msgs{re}")
        except Exception as e:
            print(f"{re}✗ Failed to forward message: {e}{re}")
        
        forward_app.stop()

    # Add message handler for the source group
    monitor_app.add_handler(MessageHandler(
        new_message_handler,
        filters.chat(groupsc)
    ))

    print(f"{gr}✅ Real-time monitoring active!{re}")
    print(f"{gr}New messages will be automatically forwarded...{re}\n")

    try:
        # Keep the monitor running
        import signal
        signal.signal(signal.SIGINT, lambda s, f: None)
        monitor_app.run()
    except KeyboardInterrupt:
        print(f"\n{ye}Stopping real-time monitoring...{re}")
        monitor_app.stop()
        print(f"{gr}Monitoring stopped!{re}")
        print(f"{cy}{'='*60}{re}")
        print(f"{gr}📊 Real-time forwarding summary:{re}")
        print(f"{gr}   Admin messages forwarded: {realtime_admin_count}{re}")
        print(f"{gr}   Regular messages forwarded: {realtime_regular_count}{re}")
        print(f"{cy}{'='*60}{re}\n")


def limicheckandrem():
    textfor = '''First, please confirm that you will never send this to strangers:
- Unsolicited advertising of any kind
- Promotional messages
- Shocking materials
Were you going to do anything like that?'''
    
    url = 'https://pastebin.com/raw/YKbeUazQ' # url of paste
    r = requests.get(url) # response will be stored from url
    content = r.text
    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            raj = app.get_me()
            textly = f'''Hello {raj.first_name}!

I’m very sorry that you had to contact me. Unfortunately, some actions can trigger a harsh response from our anti-spam systems. If you think your account was limited by mistake, you can submit a complaint to our moderators.

While the account is limited, you will not be able to send messages to people who do not have your number in their phone contacts or add them to groups and channels. Of course, when people contact you first, you can always reply to them.'''
            input_peer = "spambot"
            app.send_message(input_peer, "/start")
            time.sleep(0.5)
            for message in app.get_chat_history(input_peer, limit=1):
                print(f"{re}Bot Message: {gr}{message.text}")
            if message.text == 'Good news, no limits are currently applied to your account. You’re free as a bird!':
                app.send_message(input_peer, "Cool, thanks")
                print(f"{re}User Message: {gr}Cool, thanks")
                time.sleep(1)
                for messagee in app.get_chat_history(input_peer, limit=1):
                    print(f"{re}Bot Message: {gr}{messagee.text}")
                    print()
                    print(f"{Style.BRIGHT + ye}Conclusion: {re}No limit on your Account")
            elif message.text == 'Unfortunately, some phone numbers may trigger a harsh response from our anti-spam systems. If you think this is the case with you, you can submit a complaint to our moderators or subscribe to Telegram Premium to get less strict limits.':
                print(f"{Style.BRIGHT + ye}Review: {gr}No Limit on Account, It will cause no Problem but it can be fixed. So trying...")
                app.send_message(input_peer, "Submit a complaint")
                print(f"{re}User Message: {gr}Submit a complaint")
                time.sleep(1)
                for messagee in app.get_chat_history(input_peer, limit=1):
                    print(f"{re}Bot Message: {gr}{messagee.text}")
                    print()
                if messagee.text == textfor:
                    app.send_message(input_peer, "No, I’ll never do any of this!")
                    print(f"{re}User Message: {gr}No, I’ll never do any of this!")
                    time.sleep(1)
                    for messageee in app.get_chat_history(input_peer, limit=1):
                        print(f"{re}Bot Message: {gr}{messageee.text}")
                        print()
                        app.send_message(input_peer, content)
                        print(f"{re}User Message: {gr}{content}")
                        time.sleep(1)
                        for messageeee in app.get_chat_history(input_peer, limit=1):
                            print(f"{re}Bot Message: {gr}{messageeee.text}")
                            print()
                            print(f"{Style.BRIGHT + ye}Conclusion: {re}No limit on account but Account have harsh problem, this will not cause any problem to send message and adding members, but still a message has been sent to telegram to fix this.")
                elif messagee.text == "You've already submitted a complaint recently. Our team’s supervisors will check it as soon as possible. Thank you for your patience.":
                        print(f"{Style.BRIGHT + ye}Conclusion: {re}No limit on account but Account have harsh problem, this will not cause any problem to send message and adding members, complaint was already submitted.")
            elif message.text == textly:
                print(f"{Style.BRIGHT + ye}Review: {gr}Account Limited, Let's try to fix this.")
                app.send_message(input_peer, "This is a mistake")
                print(f"{re}User Message: {gr}This is a mistake")
                time.sleep(1)
                for messagee in app.get_chat_history(input_peer, limit=1):
                    print(f"{re}Bot Message: {gr}{messagee.text}")
                    print()
                if messagee.text == 'If you think the limitations on your account were applied by mistake, you can submit a complaint. All complaints will be reviewed by the team’s supervisor. Please note that this will have no effect on limitations that were applied with a good reason. Would you like to submit a complaint?':
                    app.send_message(input_peer, "Yes")
                    print(f"{re}User Message: {gr}Yes")
                    time.sleep(1)
                    for messageee in app.get_chat_history(input_peer, limit=1):
                        print(f"{re}Bot Message: {gr}{messageee.text}")
                        print()
                        app.send_message(input_peer, "No! Never did that!")
                        print(f"{re}User Message: {gr}No! Never did that!")
                        for messageeee in app.get_chat_history(input_peer, limit=1):
                            print(f"{re}Bot Message: {gr}{messageeee.text}")
                            print()
                            app.send_message(input_peer, content)
                            print(f"{re}User Message: {gr}{content}")
                            time.sleep(1)
                            for messageeeee in app.get_chat_history(input_peer, limit=1):
                                print(f"{re}Bot Message: {gr}{messageeeee.text}")
                                print()
                                print(f"{Style.BRIGHT + ye}Conclusion: {re}Account is Limited, We sent a message to spambot to fix this, Let's wait untill it get fixed.")
                elif messagee.text == "You've already submitted a complaint recently. Our team’s supervisors will check it as soon as possible. Thank you for your patience.":
                        print(f"{Style.BRIGHT + ye}Conclusion: {re}Account is Limited, but complaint was already submitted.")
            else:
                print(f"{wi}Account have another limti. This limit can't be removed by spambot, Please Check it.")
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number limitations will remove soon' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()



def main_menu():
    clr()
    banner()
    print(Style.BRIGHT + ye + 'Choose an Option:' + n)
    
    print(Style.BRIGHT + Fore.CYAN + '[1] Add numbers         [2] Remove banned numbers    [3] Remove numbers')
    print(Style.BRIGHT + Fore.CYAN + '[4] GC Cloner           [5] GC Cloner (Real-time)    [6] Limit Checker/Remover')
    print(Style.BRIGHT + Fore.CYAN + '[7] Account Checker     [0] Exit')

    a = int(input('\nEnter your choice: '))
    if a == 1:
        login()
    elif a == 2:
        BanFilter()
    elif a == 3:
        specificaccremove()
    elif a == 4:
        groupchatcloner_with_admin()
    elif a == 5:
        groupchatcloner_realtime()
    elif a == 6:
        limicheckandrem()
    elif a == 7:
        accountinfogetter()
    elif a == 0:
        exit()

        
main_menu()