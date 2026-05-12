import pickle, os
from time import sleep
import webbrowser
import sys
import time
import random
import pyfiglet
import logging
from pyrogram import Client
import pyrogram
import asyncio
from pyrogram.raw.functions.messages import GetWebPagePreview
from pyrogram.errors import FloodWait
from pyrogram.errors import InviteRequestSent
from pyrogram.errors import PeerFlood
from pyrogram.errors import PeerIdInvalid
from pyrogram.errors import UsernameInvalid
from pyrogram.errors import UsernameOccupied
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
import datetime
from pyrogram import types
from pyrogram.raw import functions, types
from pyrogram.enums import UserStatus
from pyrogram.errors import UserDeactivated, AuthKeyUnregistered, SessionExpired, UserDeactivatedBan
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
import string

if not os.path.exists('./sessions'):
    os.mkdir('./sessions')

try:
  from lolpython import lol_py 
  import pyfiglet
except:
  os.system("pip install lolpython")
  os.system("pip install pyfiglet")
init()

api_id = '16016703'
api_hash = "2e661b4ea5fa6d75640f12ea09f1c3a9"

n = Fore.RESET
r = Fore.RED
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
wi="\033[1,35m"

try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing module - requests...{n}')
    os.system('pip install requests')

def banner():

  os.system("clear")

  result = pyfiglet.figlet_format("          OverPowered 3.0", font = "mini"  )#chintoo
  lol_py(result) 
  lol_py('Version: 3.0 | Author: @Indian_Graphic_Designer & @JonesWarrior\n')
  print(f'{Style.BRIGHT + Fore.YELLOW} Lifetime free by @TeamTrickyAbhi')
  print()

def login():

    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            app.join_chat('@The_Hacking_Zone')
            time.sleep(4.0)
            app.join_chat('@Techno_Trickop')
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Login Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()


def directadder():
    config = configparser.ConfigParser()
    config.read("config.ini")
    groupset = config['HackingZone']['fromgroup']
    grouplink = config['HackingZone']['ToGroup']
    stopnum = config['HackingZone']['EnterStop']
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    
    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
            csv_reader = reader(delta_obj)
            list_of_phone = tuple(csv_reader)
            for phone_ in list_of_phone:
                phone.append(int(phone_[0]))
            pphone = phone

    print(f'{gr}Total account: {n} {r}{str(len(phone))}{n}')
 
    From = int(stacno) - 1
    Upto = int(endacno)


    async def mainn():
            a = 0
            indexx = 0
            for xd in pphone[From:Upto]:
                indexx += 1
                print(f'Index : {indexx}')
                phone = utils.parse_phone(xd)
                print(f"Login {phone}")
                async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:
                    await app.join_chat(groupset)
                    await app.join_chat(grouplink)
                    my_id = await app.get_chat(grouplink)
                    TARGET = await app.get_chat(groupset)
                    nu =1
                    stop = 0
                    flood = 0
                    added =0
                    peer = 0
                    userbanned = 0
                    async for targetMember in app.get_chat_members(chat_id=TARGET.id):
        
                        if stop == 50:
                            print('add 50 members bracking')
                            break
                        if flood ==5:
                            print('flood errors bracking')
                            print('total adder user ===',added)
                            break
                        if userbanned ==5:
                            print('user banned in channel errors bracking')
                            print('total adder user ===',added)
                            break
                        if peer ==5:
                            print('peer flood errors bracking')
                            print('total adder user ===',added)
                            break
                    #print(type(targetMember.user.id))
                        try:
                            await app.get_chat_member(chat_id=my_id.id, user_id=targetMember.user.id)
                        #print(k)
               
                        except UserNotParticipant as e:
                            try:
                                await app.add_chat_members(my_id.id,targetMember.user.id)
                                print('adding user ', targetMember.user.first_name,' ',targetMember.user.last_name)
                                stop = stop +1
                                added = added +1
                                time.sleep(HackingZone_dev)
                    
                            except FloodWait as e:
                                print('FloodWait',nu)
                                await asyncio.sleep(2)
                                nu = nu+1
                                flood = flood +1
                            except PeerFlood:
                                print('Peer flood error', nu)
                                await asyncio.sleep(random.randint(2,5))
                                nu = nu + 1
                                peer=peer+1
                            except UserBannedInChannel as e:
                                print('User Banned In Channel Error', nu)
                                await asyncio.sleep(random.randint(2,5))
                                nu = nu+1
                                userbanned = userbanned+1
                            except UserNotParticipant:
                                await asyncio.sleep(random.randint(2,3))
                            except UserNotMutualContact:
                                await asyncio.sleep(random.randint(2,3))
                            except UserPrivacyRestricted:
                                await asyncio.sleep(random.randint(2,3))
                            except UserChannelsTooMuch:
                                await asyncio.sleep(random.randint(2,3))
                            except Exception as e:
                                print('error',e)
                        except Exception as e:
                            print(e)
            a += 1
    asyncio.run(mainn())
    
def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



def scraper():
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    TARGET_group = config['HackingZone']['fromgroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    print(f'Total account: {str(len(phone))}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Login {phone}")
        
        if os.path.exists(f'users/{phone}.csv'):
            os.remove(f'users/{phone}.csv')
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'users/{phone}.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                try:
                    existing_members = set()
                
                    async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                        existing_members.add(my_group_member.user.id)
                    
                    async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                        if targetMember.user.id not in existing_members:
                                user_id = targetMember.user.id
                                first_name = targetMember.user.first_name or ''
                                last_name = targetMember.user.last_name or ''
                                username = targetMember.user.username or ''
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username})
                                print("user saved", first_name)
                except ChatAdminRequired as e:
                            print('Your Group Members Hidden. Unhide your group members to perform delete already filter. Press Ctrl + C to stop.')
            print('All members saved for', phone)
    async def scrape_all():
        batch_size = 8  # Number of accounts to process in each batch
        total_accounts = len(pphone)

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())


def adder():
    config = configparser.ConfigParser()
    config.read("config.ini")
    groupset = config['HackingZone']['fromgroup']
    grouplink = config['HackingZone']['ToGroup']
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']


    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())

    phone = []

    with open('phone.csv', 'r') as delta_obj:
            csv_reader = reader(delta_obj)
            list_of_phone = tuple(csv_reader)
            for phone_ in list_of_phone:
                phone.append(int(phone_[0]))
            pphone = phone

    print(f'{gr}Total account: {n} {r}{str(len(phone))}{n}')
 
    From = int(stacno) - 1
    Upto = int(endacno)

    async def mainn():
        added_members = 0
        with open('done.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for roww in reader:
                if len(roww) > 0:

                    added_members = int(roww[0])
        a = 0
        indexx = 0
        added_member = added_members 
        
        for xd in pphone[From:Upto]:
            
            indexx += 1
            print(f'Index : {indexx}')
            phone = utils.parse_phone(xd)
            print(f"Login {phone}")
            async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:
            
                try:
                #await app.join_chat(groupset)
                     await app.join_chat(grouplink)
                except UserAlreadyParticipant:
                     time.sleep(0)
                try:
                     my_id = await app.get_chat(grouplink)
                #TARGET = await app.get_chat(groupset)
                except Exception as e:
                     print('Failed to get chat entity:', e)
                     return
                
                nu =1
                stop = 0
                flood = 0
                added =0
                peer = 0
                userbanned = 0
                
                with open(f'users/{phone}.csv', mode='r', encoding='UTF-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for i, row in enumerate(csv_reader):

                        with open('done.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for roww in reader:
                                if len(roww) > 0:
                                    added_members = int(roww[0])

                        with open("done.csv", mode='w', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow([added_member+1])
                        if i < added_members:
                            continue
                        if stop == 50:
                            print('added 50 members bracking')
                            break
                        if flood ==5:
                            print('flood errors bracking')
                            print('total added user ===',added)
                            break
                        if peer ==5:
                            print('peer flood errors bracking')
                            print('total added user ===',added)
                            break
                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total added user ===', added)
                            break
                            
                        user_id = await app.resolve_peer(row['user_id'])
                        try:
                            added_member += 1
                            access_hash = user_id.access_hash
                            
                            await app.add_chat_members(my_id.id,int(user_id.user_id),access_hash)
                            print("user added",row['first_name'],row['last_name'])
                            stop = stop +1
                            added = added +1
                            time.sleep(HackingZone_dev)
                        except FloodWait as e:
                            print(f'FloodWait of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            flood = flood + 1
                            
                        except PeerFlood as e:
                            print(f'PeerFloodError of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            peer = peer + 1
                            
                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            userbanned = userbanned + 1
                            
                        except UserPrivacyRestricted as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                        except UserChannelsTooMuch as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                            
                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')

            a += 1
    asyncio.run(mainn())                  

def pvtscraper():
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    TARGET_group = str(input('Enter Private Group Link you want to Scrape: '))
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    print(f'Total account: {str(len(phone))}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Login {phone}")
        
        if os.path.exists(f'users/{phone}.csv'):
            os.remove(f'users/{phone}.csv')
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'users/{phone}.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                        try:
                            user_id = targetMember.user.id
                            first_name = targetMember.user.first_name or ''
                            last_name = targetMember.user.last_name or ''
                            username = targetMember.user.username or ''
                            writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username})
                            print("user saved", first_name)
                        except ChatAdminRequired as e:
                            print('Your Group Members Hidden. Unhide your group members to perform delete already filter. Press Ctrl + C to stop.')
            print('All members saved for', phone)
    async def scrape_all():
        batch_size = 8  # Number of accounts to process in each batch
        total_accounts = len(pphone)

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())


def hiddenscraper():
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    TARGET_group = config['HackingZone']['fromgroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    print(Style.BRIGHT + Fore.GREEN + f'This option scrape messages of group after scraping message it print sender id, sender username, everything of message in data.csv, this is how this option scrape hidden members of Group No fill below information if you understand this.')
    
    scrlimit = int(input(f'{cy}Enter how many message you want to scrape to get hidden members{r}'))
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()   
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            my_group_members = set()
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
                
                async for participant in app.get_chat_members(chat_id=my_id.id):
                    my_group_members.add(participant.user.id)
                    
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = {}

                async for message in app.get_chat_history(TARGET.id, limit=scrlimit):
                    if not message.from_user or message.from_user.is_bot:
                # Skip messages from channels and bots
                       continue
                    user = await app.get_users(message.from_user.id)

                    if user is not None:
                        user_id = user.id
                        first_name = user.first_name or ''
                        last_name = user.last_name or ''
                        username = user.username or ''
                        if username:
                    # Check if the user ID is already saved in the CSV
                            if user_id not in existing_members:
                                existing_members[user_id] = {
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'username': username
                                }
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username})
                                print("User saved:", first_name, last_name, username)
                        else:
                               time.sleep(0)

                print('All members saved for', phone)

            # Get all members in your group

            # Remove user IDs that are already in your group
                existing_members = {user_id: user_info for user_id, user_info in existing_members.items() if user_id not in my_group_members}

                if os.path.exists(f'data.csv'):
                    os.remove(f'data.csv')

            # Save the user IDs that are not in your group
                with open(f'data.csv', encoding='UTF-8', mode='a', newline='') as csv_file:
                    fieldnames = ['user_id', 'first_name', 'last_name', 'username']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for user_id, user_info in existing_members.items():
                        writer.writerow({
                            'user_id': user_id,
                            'first_name': user_info['first_name'],
                            'last_name': user_info['last_name'],
                            'username': user_info['username']
                        })

                print('Non-group members saved for', phone)
                
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())


def pvthiddenscraper():
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    TARGET_group = str(input('Enter Private Group Link you want to Scrape: '))
    
    print(Style.BRIGHT + Fore.GREEN + f'This option scrape messages of group after scraping message it print sender id, sender username, everything of message in data.csv, this is how this option scrape hidden members of Group No fill below information if you understand this.')
    
    scrlimit = int(input(f'{cy}Enter how many message you want to scrape to get hidden members{r}'))
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            my_group_members = set()
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
                
                async for participant in app.get_chat_members(chat_id=my_id.id):
                    my_group_members.add(participant.user.id)
                    
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = {}

                # Get all messages in the target group
                async for message in app.get_chat_history(TARGET.id, limit=scrlimit):
                    if not message.from_user or message.from_user.is_bot:
                # Skip messages from channels and bots
                       continue
                    user = await app.get_users(message.from_user.id)

                    if user is not None:
                        user_id = user.id
                        first_name = user.first_name or ''
                        last_name = user.last_name or ''
                        username = user.username or ''
                        if username:
                    # Check if the user ID is already saved in the CSV
                            if user_id not in existing_members:
                                existing_members[user_id] = {
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'username': username
                                }
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username})
                                print("User saved:", first_name, last_name, username)
                        else:
                               time.sleep(0)

                print('All members saved for', phone)

            # Get all members in your group

            # Remove user IDs that are already in your group
                existing_members = {user_id: user_info for user_id, user_info in existing_members.items() if user_id not in my_group_members}

                if os.path.exists(f'data.csv'):
                    os.remove(f'data.csv')

            # Save the user IDs that are not in your group
                with open(f'data.csv', encoding='UTF-8', mode='a', newline='') as csv_file:
                    fieldnames = ['user_id', 'first_name', 'last_name', 'username']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for user_id, user_info in existing_members.items():
                        writer.writerow({
                            'user_id': user_id,
                            'first_name': user_info['first_name'],
                            'last_name': user_info['last_name'],
                            'username': user_info['username']
                        })

                print('Non-group members saved for', phone)
                
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def pvtadder():
    config = configparser.ConfigParser()
    config.read("config.ini")
    groupset = config['HackingZone']['fromgroup']
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']

    grouplink = str(input('Enter Private Group Link where you want to Add Members: '))

    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())

    phone = []

    with open('phone.csv', 'r') as delta_obj:
            csv_reader = reader(delta_obj)
            list_of_phone = tuple(csv_reader)
            for phone_ in list_of_phone:
                phone.append(int(phone_[0]))
            pphone = phone

    print(f'{gr}Total account: {n} {r}{str(len(phone))}{n}')
 
    From = int(stacno) - 1
    Upto = int(endacno)

    async def mainn():
        added_members = 0
        with open('done.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for roww in reader:
                if len(roww) > 0:

                    added_members = int(roww[0])
        a = 0
        indexx = 0
        added_member = added_members 
        
        for xd in pphone[From:Upto]:
            
            indexx += 1
            print(f'Index : {indexx}')
            phone = utils.parse_phone(xd)
            print(f"Login {phone}")
            async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:
                try:
                #await app.join_chat(groupset)
                     await app.join_chat(grouplink)
                except UserAlreadyParticipant:
                     time.sleep(0)
                try:
                     my_id = await app.get_chat(grouplink)
                #TARGET = await app.get_chat(groupset)
                except Exception as e:
                     print('Failed to get chat entity:', e)
                     return
                
                nu =1
                stop = 0
                flood = 0
                added =0
                peer = 0
                userbanned = 0
                
                with open(f'users/{phone}.csv', mode='r', encoding='UTF-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for i, row in enumerate(csv_reader):

                        with open('done.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for roww in reader:
                                if len(roww) > 0:
                                    added_members = int(roww[0])

                        with open("done.csv", mode='w', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow([added_member+1])
                        if i < added_members:
                            continue
                        if stop == 50:
                            print('added 50 members bracking')
                            break
                        if flood ==5:
                            print('flood errors bracking')
                            print('total added user ===',added)
                            break
                        if peer ==5:
                            print('peer flood errors bracking')
                            print('total added user ===',added)
                            break
                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total added user ===', added)
                            break
                            
                        user_id = await app.resolve_peer(row['user_id'])
                        try:
                            added_member += 1
                            access_hash = user_id.access_hash
                            
                            await app.add_chat_members(my_id.id,int(user_id.user_id),access_hash)
                            print("user added",row['first_name'],row['last_name'])
                            stop = stop +1
                            added = added +1
                            time.sleep(HackingZone_dev)
                        except FloodWait as e:
                            print(f'FloodWait of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            flood = flood + 1
                            
                        except PeerFlood as e:
                            print(f'PeerFloodError of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            peer = peer + 1
                            
                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            userbanned = userbanned + 1
                            
                        except UserPrivacyRestricted as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                        except UserChannelsTooMuch as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                            
                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')

            a += 1
    asyncio.run(mainn())                  

def dailyfilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    TARGET_group = config['HackingZone']['fromgroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
        
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.ONLINE:
                                        status = 'Online'
                                    elif entity.status == UserStatus.RECENTLY:
                                        status = 'Recently Seen'
                                    elif entity.status == UserStatus.OFFLINE:
                                        d = entity.last_online_date
                                        today_user = d.day == today.day and d.month == today.month and d.year == today.year
                                        yesterday_user = d.day == yesterday.day and d.month == yesterday.month and d.year == yesterday.year
                                        if today_user or yesterday_user:
                                            status = d or type(entity.last_online_date).__name__
                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                        else:
                            time.sleep(0)

        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1 # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())
    
def pvtdailyfilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    TARGET_group = str(input('Enter Private Group Link you want to Scrape: '))
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
        
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping From {phone}")
        
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.ONLINE:
                                        status = 'Online'
                                    elif entity.status == UserStatus.RECENTLY:
                                        status = 'Recently Seen'
                                    elif entity.status == UserStatus.OFFLINE:
                                        d = entity.last_online_date
                                        today_user = d.day == today.day and d.month == today.month and d.year == today.year
                                        yesterday_user = d.day == yesterday.day and d.month == yesterday.month and d.year == yesterday.year
                                        if today_user or yesterday_user:
                                            status = d or type(entity.last_online_date).__name__
                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                        else:
                            time.sleep(0)

        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1 # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def weeklyfilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    TARGET_group = config['HackingZone']['fromgroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
        
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone


    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping From {phone}")
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.ONLINE:
                                        status = 'Online'
                                    elif entity.status == UserStatus.RECENTLY:
                                        status = 'Recently Seen'
                                    elif entity.status == UserStatus.LAST_WEEK:
                                        status = 'Last Week'
                                    elif entity.status == UserStatus.OFFLINE:
                                        d = entity.last_online_date
                                        for i in range(0,7):
                                            current_day = today - datetime.timedelta(days=i)
                                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                                            if correct_user:
                                                status = d or type(entity.last_online_date).__name__
                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                                
                        else:
                            time.sleep(0)

        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def pvtweeklyfilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    TARGET_group = str(input('Enter Private Group Link you want to Scrape: '))
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
        
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.ONLINE:
                                        status = 'Online'
                                    elif entity.status == UserStatus.RECENTLY:
                                        status = 'Recently Seen'
                                    elif entity.status == UserStatus.LAST_WEEK:
                                        status = 'Last Week'
                                    elif entity.status == UserStatus.OFFLINE:
                                        d = entity.last_online_date
                                        for i in range(0,7):
                                            current_day = today - datetime.timedelta(days=i)
                                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                                            if correct_user:
                                                status = d or type(entity.last_online_date).__name__
                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                                
                        else:
                            time.sleep(0)

        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def monthlyfilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    TARGET_group = config['HackingZone']['fromgroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone


    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.ONLINE:
                                        status = 'Online'
                                    elif entity.status == UserStatus.RECENTLY:
                                        status = 'Recently Seen'
                                    elif entity.status == UserStatus.LAST_WEEK:
                                        status = 'Last Week'
                                    elif entity.status == UserStatus.LAST_MONTH:
                                        status = 'Last Month'
                                    elif entity.status == UserStatus.OFFLINE:
                                        d = entity.last_online_date
                                        for i in range(0,30):
                                            current_day = today - datetime.timedelta(days=i)
                                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                                            if correct_user:
                                                status = d or type(entity.last_online_date).__name__

                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                        else:
                            time.sleep(0)
                            
        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())
    
def pvtmonthlyfilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    TARGET_group = config['HackingZone']['fromgroup']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
        
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
        
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.ONLINE:
                                        status = 'Online'
                                    elif entity.status == UserStatus.RECENTLY:
                                        status = 'Recently Seen'
                                    elif entity.status == UserStatus.LAST_WEEK:
                                        status = 'Last Week'
                                    elif entity.status == UserStatus.LAST_MONTH:
                                        status = 'Last Month'
                                    elif entity.status == UserStatus.OFFLINE:
                                        d = entity.last_online_date
                                        for i in range(0,30):
                                            current_day = today - datetime.timedelta(days=i)
                                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                                            if correct_user:
                                                status = d or type(entity.last_online_date).__name__

                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                        else:
                            time.sleep(0)
                            
        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def inactivefilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    TARGET_group = config['HackingZone']['fromgroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone


    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.LONG_AGO:
                                        status = 'Long Ago'
                                    if entity.status == UserStatus.OFFLINE:
                                        d = entity.last_online_date.timestamp()
                                        last_active_date = datetime.datetime.fromtimestamp(d)
                                        thirty_days_ago_timestamp = (today - datetime.timedelta(days=30)).timestamp()

                                        if last_active_date.timestamp() <= thirty_days_ago_timestamp:
                                             status = 'Non-Active' or f'Last Seen on {last_active_date}'

                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                        else:
                            time.sleep(0)
        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())


def pvtinactivefilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    TARGET_group = config['HackingZone']['fromgroup']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.LONG_AGO:
                                        status = 'Long Ago'
                                    if entity.status == UserStatus.OFFLINE:
                                        d = entity.last_online_date.timestamp()
                                        last_active_date = datetime.datetime.fromtimestamp(d)
                                        thirty_days_ago_timestamp = (today - datetime.timedelta(days=30)).timestamp()

                                        if last_active_date.timestamp() <= thirty_days_ago_timestamp:
                                             status = 'Non-Active' or f'Last Seen on {last_active_date}'

                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                        else:
                            time.sleep(0)
        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def onlinefilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    TARGET_group = config['HackingZone']['fromgroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone


    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.ONLINE:
                                        status = 'Online'

                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                        else:
                            time.sleep(0)
        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def pvtonlinefilter():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    TARGET_group = config['HackingZone']['fromgroup']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
        
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.status:
                                    if entity.status == UserStatus.ONLINE:
                                        status = 'Online'

                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                        else:
                            time.sleep(0)
        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def contactadder():
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']

    print('Enter Delay Time Per Request 0 For None: ')
    HackingZone_dev = int(input())

    phone = []
    added_users = set()  # Set to track added users

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(phone_[0])
        pphone = phone

    print(f'Total accounts: {str(len(phone))}')

    async def mainn(xd, start_row, end_row):
        phone = utils.parse_phone(xd)
        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            nu = 1
            stop = 0
            flood = 0
            added = 0
            peer = 0
            userbanned = 0

            with open(f'users/{phone}.csv', mode='r', encoding='UTF-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                # Skip to the specified start_row
                for _ in range(start_row):
                    next(csv_reader)

                for row in csv_reader:

                    if flood == 5:
                        print('flood errors breaking')
                        print('total added contact ===', added)
                        break

                    if peer == 5:
                        print('peer flood errors breaking')
                        print('total added contact ===', added)
                        break

                    if userbanned == 5:
                        print('UserBannedInChannelError errors breaking')
                        print('total added contact ===', added)
                        break

                    user_id = int(row['user_id'])

                    try:
                        await app.add_contact(user_id, row['first_name'])

                        print("Contact added", row['first_name'], row['last_name'])
                        added = added + 1
                        time.sleep(HackingZone_dev)

                        if added == 80:  # 80 rows added for this account, break
                            print('80 contacts added for this account, breaking')
                            break

                    except UserPrivacyRestricted as e:
                        await asyncio.sleep(random.randint(2, 3))

                    except UserChannelsTooMuch:
                        await asyncio.sleep(0)

                    except PeerFlood as e:
                        print('PeerFloodError', nu)
                        await asyncio.sleep(random.randint(2, 5))
                        nu = nu + 1
                        peer = peer + 1

                    except UserBannedInChannel as e:
                        print('User Banned In Channel Error', nu)
                        await asyncio.sleep(random.randint(2, 5))
                        nu = nu + 1
                        userbanned = userbanned + 1

                    except FloodWait as e:
                        print('FloodWait', nu)
                        await asyncio.sleep(random.randint(2, 5))
                        nu = nu + 1
                        flood = flood + 1

                    except RPCError as e:
                        status = e.__class__.__name__
                        print(f'{status}')

                    except:
                        traceback.print_exc()
                        print("Unexpected Error")

    async def scrape_all():
        batch_size = 8  # Number of accounts to process in each batch
        total_accounts = len(pphone)

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = []

            for idx, phone_num in enumerate(batch):
                start_row = i * 80 + idx * 80 + 1
                end_row = start_row + 80

                task = mainn(phone_num, start_row, end_row)
                tasks.append(task)

            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())
    
def contactdeleter():
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']

    print('Enter Delay Time Per Request 0 For None: ')
    HackingZone_dev = int(input())

    phone = []
    added_users = set()
    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(phone_[0])
        pphone = phone

    print(f'Total accounts: {str(len(phone))}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:
            
            nu = 1
            flood = 0
            peer = 0
            added = 0
            userbanned = 0
            
            contacts = await app.get_contacts()
            #contacts = await client(GetContactsRequest(hash=0))
            rexadd = 0
            for contact in contacts:
                rexadd += 1
                
                if flood == 5:
                     print(f'flood errors on {phone} breaking')
                     print(f'total deleted contact by {phone} ===', added)
                     break

                if peer == 5:
                     print(f'peer flood errors on {phone} breaking')
                     print(f'total deleted contact by {phone} ===', added)
                     break

                if userbanned == 5:
                     print(f'UserBannedInChannelError errors on {phone} breaking')
                     print(f'total deleted contact by {phone} ===', added)
                     break

                try:
                     await app.delete_contacts(contact.id)
                     print(Style.BRIGHT + Fore.GREEN + f"{rexadd} - {contact.id} - DELETE in {phone}")
                     added = added + 1
                     time.sleep(HackingZone_dev)

                except UserPrivacyRestricted as e:
                     await asyncio.sleep(random.randint(2, 3))

                except UserChannelsTooMuch:
                     await asyncio.sleep(0)

                except PeerFlood:
                     print(f'{rexadd} - {contact.id} - PeerFloodError on {phone}', nu)
                     await asyncio.sleep(random.randint(2, 5))
                     nu = nu + 1
                     peer = peer + 1

                except UserBannedInChannel as e:
                     print(f'{rexadd} - {contact.id} - User Banned In Channel Error on {phone}', nu)
                     await asyncio.sleep(random.randint(2, 5))
                     nu = nu + 1
                     userbanned = userbanned + 1

                except FloodWait as e:
                     print(f'{rexadd} - {contact.id} - FloodWait on {phone}', nu)
                     await asyncio.sleep(random.randint(2, 5))
                     nu = nu + 1
                     flood = flood + 1

                except RPCError as e:
                     erro = e.__class__.__name__
                     print(f'{rexadd} - {contact.id} - {erro} on {phone}')
                     continue

                except:
                     traceback.print_exc()
                     print("Unexpected Error")

    async def scrape_all():
        batch_size = 8  # Number of accounts to process in each batch
        total_accounts = len(pphone)

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def bulkaddermulti():
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    print(Style.BRIGHT + Fore.GREEN + 'In A Batch How many Members You Want To Add : ')
    Legenddevismain = int(input())
    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev =int(input())

    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    print(f'Total account: {str(len(phone))}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")
        
        if os.path.exists(f'users/{phone}.csv'):
            os.remove(f'users/{phone}.csv')

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                #await app.join_chat(groupset)
                     await app.join_chat(my_group)
            except UserAlreadyParticipant:
                     time.sleep(0)
            try:
                     my_id = await app.get_chat(my_group)
            except Exception as e:
                     print('Failed to get chat entity:', e)
                     return

            nu = 1
            flood = 0
            peer = 0
            userbanned = 0
            
            contacts = await app.get_contacts()
            #members = await client(GetContactsRequest(hash=0))
            #user_to_add = members.users
            user_to_add = []
            for contact in contacts:
                user_to_add.append(contact.id)
            countcon = len(user_to_add)
            print(f'Total : {countcon}')

            batchcount = 0
            lol = 0
            while batchcount < countcon:
            
                 if flood == 5:
                     print(f'flood errors on {phone} breaking')
                     break
                 if peer == 5:
                     print(f'peer flood errors on {phone} breaking')
                     break
                 if userbanned == 5:
                     print(f'UserBannedInChannelError errors on {phone} breaking')
                     break

                 semen = [delta for delta in user_to_add[:Legenddevismain]]
                 try:
                     time.sleep(HackingZone_dev)
                     await app.add_chat_members(my_id.id,semen)
                     batchcount += Legenddevismain
                     for i in range(0, 15):
                        try:
                            del user_to_add[i]
                        except Exception as D:
                            continue
                     print(Style.BRIGHT + Fore.GREEN + f'BATCH: {batchcount} by {phone}')
                 except PeerFlood as e:
                     print(f'PeerFloodError on {phone}', nu)
                     await asyncio.sleep(random.randint(2, 5))
                     nu = nu + 1
                     peer = peer + 1

                 except UserBannedInChannel as e:
                     print(f'User Banned In Channel Error on {phone}', nu)
                     await asyncio.sleep(random.randint(2, 5))
                     nu = nu + 1
                     userbanned = userbanned + 1

                 except FloodWait as e:
                     print(f'FloodWait on {phone}', nu)
                     await asyncio.sleep(random.randint(2, 5))
                     nu = nu + 1
                     flood = flood + 1
                     
                 except RPCError as e:
                      erro = e.__class__.__name__
                      print(str(erro))
                      break


    async def scrape_all():
        batch_size = 8  # Number of accounts to process in each batch
        total_accounts = len(pphone)

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def BanFilter():

    MadeByHackingZone = []

    done = False
    with open('phone.csv', 'r') as f:
        str_list = [row[0] for row in csv.reader(f)]

        po = 0
        for unparsed_phone in str_list:
            po += 1

            phone = utils.parse_phone(unparsed_phone)

            print(f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            # client.start(phone)
            try:
                    app.start()
                    continue

            except AuthKeyUnregistered:
                    print('Session Revoked')
                    HackingZone = str(po)
                    Nero_op = str(unparsed_phone)
                    MadeByHackingZone.append(Nero_op)
                    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
                         writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

                         writer.writerows(MadeByHackingZone)

            except UserDeactivatedBan:
                    print('Ban')
                    HackingZone = str(po)
                    Nero_op = str(unparsed_phone)
                    MadeByHackingZone.append(Nero_op)
                    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
                         writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

                         writer.writerows(MadeByHackingZone)
                         
            except SessionExpired:
                    print('Session Expired')
                    HackingZone = str(po)
                    Nero_op = str(unparsed_phone)
                    MadeByHackingZone.append(Nero_op)
                    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
                         writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

                         writer.writerows(MadeByHackingZone)
                         
            except UserDeactivated:
                    print('User Deactivated')
                    HackingZone = str(po)
                    Nero_op = str(unparsed_phone)
                    MadeByHackingZone.append(Nero_op)
                    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
                         writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

                         writer.writerows(MadeByHackingZone)

                    continue

            # client.disconnect()
        done = True
        print('List Of Banned Numbers')
        print(*MadeByHackingZone, sep='\n')
        print('Saved In BanNumers.csv')


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

def permanentlimitremover():

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
            input_peer = "spambot"
            app.send_message(input_peer, "/start")
            time.sleep(0.5)
            app.send_message(input_peer, "Submit a complaint")
            time.sleep(0.5)
            app.send_message(input_peer, "No, I’ll never do any of this!")
            time.sleep(0.5)
            app.send_message(input_peer, content)
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number limitations will remove soon' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def permanentlimitremover2():

    url = 'https://pastebin.com/raw/9GFDwMcV' # url of paste
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
            input_peer = "spambot"
            app.send_message(input_peer, "/start")
            time.sleep(0.5)
            app.send_message(input_peer, "This is a mistake")
            time.sleep(0.5)
            app.send_message(input_peer, "Yes")
            time.sleep(0.5)
            app.send_message(input_peer, "No! Never did that!")
            time.sleep(0.5)
            app.send_message(input_peer, content)
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number limitations will remove soon' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

    
def otpviewer():

   with open('phone.csv', 'r') as f:
    str_list = [row[0] for row in csv.reader(f)]
    for pphone in str_list:
        phone = utils.parse_phone(pphone)
        app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
        app.start()
        print(f"{r} Getting Telegram message OTP for {phone}")
        try:
            # Get the latest message from the chat
            for message in app.get_chat_history(777000, limit=1):
                print(f"{ye}{message.text}")
            else:
                print("No messages found in chat history.")
        except RPCError as e:
            print(f"An error occurred: {e}.")
        app.stop()
        print()
        print("Enter to go to next account")
        input()
    print(f"{gr}Type Enter to go to main menu")
    input()

def bulkadder():
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    print(Style.BRIGHT + Fore.GREEN + 'In A Batch How many Members You Want To Add : ')
    Legenddevismain = int(input())
    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev =int(input())

    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    print(f'Total account: {str(len(phone))}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")
        
        if os.path.exists(f'users/{phone}.csv'):
            os.remove(f'users/{phone}.csv')

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                #await app.join_chat(groupset)
                     await app.join_chat(my_group)
            except UserAlreadyParticipant:
                     time.sleep(0)
            try:
                     my_id = await app.get_chat(my_group)
            except Exception as e:
                     print('Failed to get chat entity:', e)
                     return

            nu = 1
            flood = 0
            peer = 0
            userbanned = 0
            
            contacts = await app.get_contacts()
            #members = await client(GetContactsRequest(hash=0))
            #user_to_add = members.users
            user_to_add = []
            for contact in contacts:
                user_to_add.append(contact.id)
            countcon = len(user_to_add)
            print(f'Total : {countcon}')

            batchcount = 0
            lol = 0
            while batchcount < countcon:
            
                 if flood == 5:
                     print(f'flood errors on {phone} breaking')
                     break
                 if peer == 5:
                     print(f'peer flood errors on {phone} breaking')
                     break
                 if userbanned == 5:
                     print(f'UserBannedInChannelError errors on {phone} breaking')
                     break

                 semen = [delta for delta in user_to_add[:Legenddevismain]]
                 try:
                     time.sleep(HackingZone_dev)
                     await app.add_chat_members(my_id.id,semen)
                     batchcount += Legenddevismain
                     for i in range(0, 15):
                        try:
                            del user_to_add[i]
                        except Exception as D:
                            continue
                     print(Style.BRIGHT + Fore.GREEN + f'BATCH: {batchcount} by {phone}')
                 except PeerFlood as e:
                     print(f'PeerFloodError on {phone}', nu)
                     await asyncio.sleep(random.randint(2, 5))
                     nu = nu + 1
                     peer = peer + 1

                 except UserBannedInChannel as e:
                     print(f'User Banned In Channel Error on {phone}', nu)
                     await asyncio.sleep(random.randint(2, 5))
                     nu = nu + 1
                     userbanned = userbanned + 1

                 except FloodWait as e:
                     print(f'FloodWait on {phone}', nu)
                     await asyncio.sleep(random.randint(2, 5))
                     nu = nu + 1
                     flood = flood + 1
                     
                 except RPCError as e:
                      erro = e.__class__.__name__
                      print(str(erro))
                      break


    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = len(pphone)

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def MultiAdderFunction():
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    grouplink = config['HackingZone']['ToGroup']

    print('Enter Delay Time Per Request 0 For None: ')
    HackingZone_dev = int(input())

    phone = []
    added_users = set()  # Set to track added users

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(phone_[0])
        pphone = phone

    print(f'Total accounts: {str(len(phone))}')

    async def mainn(xd, start_row, end_row):
        phone = utils.parse_phone(xd)
        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:
        
            try:
                #await app.join_chat(groupset)
                     await app.join_chat(grouplink)
            except UserAlreadyParticipant:
                     time.sleep(0)
            try:
                     my_id = await app.get_chat(grouplink)
                #TARGET = await app.get_chat(groupset)
            except Exception as e:
                     print('Failed to get chat entity:', e)
                     return

            nu = 1
            stop = 0
            flood = 0
            added = 0
            peer = 0
            userbanned = 0

            with open(f'users/{phone}.csv', mode='r', encoding='UTF-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                # Skip to the specified start_row
                for _ in range(start_row):
                    next(csv_reader)

                for row in csv_reader:

                    if flood == 5:
                        print('flood errors breaking')
                        print('total added users ===', added)
                        break

                    if peer == 5:
                        print('peer flood errors breaking')
                        print('total added users ===', added)
                        break

                    if userbanned == 5:
                        print('UserBannedInChannelError errors breaking')
                        print('total added users ===', added)
                        break

                    user_id = await app.resolve_peer(row['user_id'])

                    try:
                        access_hash = user_id.access_hash
                            
                        await app.add_chat_members(my_id.id,int(user_id.user_id),access_hash)
                        print("user added",row['first_name'],row['last_name'])
                        added = added + 1
                        time.sleep(HackingZone_dev)

                        if added == 50:  # 80 rows added for this account, break
                            print('50 users added for this account, breaking')
                            break

                    except UserPrivacyRestricted as e:
                        await asyncio.sleep(random.randint(2, 3))

                    except UserChannelsTooMuch:
                        await asyncio.sleep(0)

                    except PeerFlood as e:
                        print('PeerFloodError', nu)
                        await asyncio.sleep(random.randint(2, 5))
                        nu = nu + 1
                        peer = peer + 1

                    except UserBannedInChannel as e:
                        print('User Banned In Channel Error', nu)
                        await asyncio.sleep(random.randint(2, 5))
                        nu = nu + 1
                        userbanned = userbanned + 1

                    except FloodWait as e:
                        print('FloodWait', nu)
                        await asyncio.sleep(random.randint(2, 5))
                        nu = nu + 1
                        flood = flood + 1

                    except RPCError as e:
                        status = e.__class__.__name__
                        print(f'{status}')

                    except:
                        traceback.print_exc()
                        print("Unexpected Error")

    async def scrape_all():
        batch_size = 8  # Number of accounts to process in each batch
        total_accounts = len(pphone)

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = []

            for idx, phone_num in enumerate(batch):
                start_row = i * 90 + idx * 90 + 1
                end_row = start_row + 90

                task = mainn(phone_num, start_row, end_row)
                tasks.append(task)

            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def multi_ccraper():
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    TARGET_group = config['HackingZone']['fromgroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
        
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    #print(f'Total account: {str(len(phone))}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping From {phone}")
        
        if os.path.exists(f'users/{phone}.csv'):
            os.remove(f'users/{phone}.csv')
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(1)
            my_id = await app.get_chat(my_group)
            TARGET = await app.get_chat(TARGET_group)
            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    try:
                        await app.get_chat_member(chat_id=my_id.id, user_id=targetMember.user.id)
                    except UserNotParticipant as e:
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        
                        if username:  # Check if the username exists
                             writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username})
                             print("user saved", first_name)
                        else:
                             time.sleep(0)
            print('All members saved for', phone)
   
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def groupjoiner():

    print('Enter Group/Channel Username:  ')
    usernamehh = str(input())
    print('Enter Delay Time Per Request 0 For None: ')
    HackingZone_dev = int(input())
    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            try:
               app.start()
               app.join_chat(usernamehh)
               print('Join Successful')
            except UserAlreadyParticipant:
                print("You are already Participant of this Chat")
                time.sleep(0)
            except InviteRequestSent:
                print("Request Already Sent")
                time.sleep(0)
            app.stop()
            time.sleep(HackingZone_dev)
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Login Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def grouplefter():

    print(f'{gr}Enter Group/Channel Username:  ')
    usernamehh = str(input())
    print(f'{gr}Enter Delay Time Per Request 0 For None: ')
    HackingZone_dev = int(input())
    lowercase_input = usernamehh.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot leave this channel')
         exit()
    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            try:
               app.start()
               app.leave_chat(usernamehh)
               print(f'{wi}Left Successful')
            except UserNotParticipant:
                time.sleep(0)
            app.stop()
            time.sleep(HackingZone_dev)
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Leave Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def filterwalaadder():
    config = configparser.ConfigParser()
    config.read("config.ini")
    groupset = config['HackingZone']['fromgroup']
    grouplink = config['HackingZone']['ToGroup']
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']


    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())

    phone = []

    with open('phone.csv', 'r') as delta_obj:
            csv_reader = reader(delta_obj)
            list_of_phone = tuple(csv_reader)
            for phone_ in list_of_phone:
                phone.append(int(phone_[0]))
            pphone = phone

    print(f'{gr}Total account: {n} {r}{str(len(phone))}{n}')
 
    From = int(stacno) - 1
    Upto = int(endacno)

    async def mainn():
        added_members = 0
        with open('done.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for roww in reader:
                if len(roww) > 0:

                    added_members = int(roww[0])
        a = 0
        indexx = 0
        added_member = added_members 
        
        for xd in pphone[From:Upto]:
            
            indexx += 1
            print(f'Index : {indexx}')
            phone = utils.parse_phone(xd)
            print(f"Login {phone}")
            async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:
            
                try:
                #await app.join_chat(groupset)
                     await app.join_chat(grouplink)
                except UserAlreadyParticipant:
                     time.sleep(0)
                try:
                     my_id = await app.get_chat(grouplink)
                #TARGET = await app.get_chat(groupset)
                except Exception as e:
                     print('Failed to get chat entity:', e)
                     return
                
                nu =1
                stop = 0
                flood = 0
                added =0
                peer = 0
                userbanned = 0
                
                with open(f'data.csv', mode='r', encoding='UTF-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for i, row in enumerate(csv_reader):

                        with open('done.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for roww in reader:
                                if len(roww) > 0:
                                    added_members = int(roww[0])

                        with open("done.csv", mode='w', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow([added_member+1])
                        if i < added_members:
                            continue
                        if stop == 50:
                            print('added 50 members bracking')
                            break
                        if flood ==5:
                            print('flood errors bracking')
                            print('total added user ===',added)
                            break
                        if peer ==5:
                            print('peer flood errors bracking')
                            print('total added user ===',added)
                            break
                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total added user ===', added)
                            break
                            
                        username = row['username']
                        try:
                            added_member += 1
                            await app.add_chat_members(my_id.id,str(username))
                            print("user added",row['first_name'],row['last_name'])
                            stop = stop +1
                            added = added +1
                            time.sleep(HackingZone_dev)
                        except FloodWait as e:
                            print(f'FloodWait of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            flood = flood + 1
                            
                        except PeerFlood as e:
                            print(f'PeerFloodError of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            peer = peer + 1
                            
                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            userbanned = userbanned + 1
                            
                        except UserPrivacyRestricted as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                        except UserChannelsTooMuch as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                            
                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')

            a += 1
    asyncio.run(mainn())                  

def reactionincreaser():

    print('Enter Group/Channel Username:  ')
    usernamehh = str(input())
    msgid = int(input('Enter Message/Post ID: '))
    reactionty = str(input('Enter Reaction: '))
    print('Enter Delay Time Per Request 0 For None: ')
    HackingZone_dev = int(input())
    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Using {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            try:
               app.start()
               app.join_chat(usernamehh)
            except UserAlreadyParticipant:
                time.sleep(0)
            app.send_reaction(usernamehh, msgid, reactionty)
            print(f'Successfull Reaction from {phone}')
            app.stop()
            time.sleep(HackingZone_dev)
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Login Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def sharesincreaser():

    print('Enter Group/Channel Username:  ')
    usernamehh = str(input())
    msgid = int(input('Enter Message/Post ID: '))
    print('Enter Delay Time Per Request 0 For None: ')
    HackingZone_dev = int(input())
    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Using {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            try:
               app.start()
               app.join_chat(usernamehh)
            except UserAlreadyParticipant:
                time.sleep(0)
            try:
                my_id = app.get_chat(usernamehh)
            except Exception as e:
                print('Failed to get chat entity:', e)
                
            app.forward_messages(chat_id="me", from_chat_id=my_id.id, message_ids=msgid)
            print(f'Successfull shares from {phone}')
            app.stop()
            time.sleep(HackingZone_dev)
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Login Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def massdm():
    config = configparser.ConfigParser()
    config.read("config.ini")
    groupset = config['HackingZone']['fromgroup']
    grouplink = config['HackingZone']['ToGroup']
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']

    mssg = str(input('Enter Message you want to send: '))

    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())

    phone = []

    with open('phone.csv', 'r') as delta_obj:
            csv_reader = reader(delta_obj)
            list_of_phone = tuple(csv_reader)
            for phone_ in list_of_phone:
                phone.append(int(phone_[0]))
            pphone = phone

    print(f'{gr}Total account: {n} {r}{str(len(phone))}{n}')
 
    From = int(stacno) - 1
    Upto = int(endacno)

    async def mainn():
        added_members = 0
        with open('done.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for roww in reader:
                if len(roww) > 0:

                    added_members = int(roww[0])
        a = 0
        indexx = 0
        added_member = added_members 
        
        for xd in pphone[From:Upto]:
            
            indexx += 1
            print(f'Index : {indexx}')
            phone = utils.parse_phone(xd)
            print(f"Login {phone}")
            async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:
                
                nu =1
                stop = 0
                flood = 0
                added =0
                peer = 0
                userbanned = 0
                
                with open(f'data.csv', mode='r', encoding='UTF-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for i, row in enumerate(csv_reader):

                        with open('done.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for roww in reader:
                                if len(roww) > 0:
                                    added_members = int(roww[0])

                        with open("done.csv", mode='w', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow([added_member+1])
                        if i < added_members:
                            continue
                        if stop == 50:
                            print('added 50 members bracking')
                            break
                        if flood ==5:
                            print('flood errors bracking')
                            print('total added user ===',added)
                            break
                        if peer ==5:
                            print('peer flood errors bracking')
                            print('total added user ===',added)
                            break
                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total added user ===', added)
                            break
                            
                        username = row['username']
                        try:
                            added_member += 1
                            await app.send_message(str(username), mssg)
                            print("user added",row['first_name'],row['last_name'])
                            stop = stop +1
                            added = added +1
                            time.sleep(HackingZone_dev)
                        except FloodWait as e:
                            print(f'FloodWait of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            flood = flood + 1
                            
                        except PeerFlood as e:
                            print(f'PeerFloodError of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            peer = peer + 1
                            
                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            userbanned = userbanned + 1
                            
                        except UserPrivacyRestricted as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                        except UserChannelsTooMuch as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                            
                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')

            a += 1
    asyncio.run(mainn())                  

def autoidcloner():

     def send_clones_from_csv(phone_csv_path, clones_csv_path):
          with open(phone_csv_path, 'r') as phone_file, open(clones_csv_path, 'r') as clones_file:
              phone_reader = csv.reader(phone_file)
              clones_reader = csv.reader(clones_file)
        
              phone_rows = list(phone_reader)
              clones_rows = list(clones_reader)

              if len(phone_rows) != len(clones_rows):
                  print("Error: The number of rows in 'phone.csv' and 'clone.csv' is not equal.")
                  return

              for phone_row, clones_row in zip(phone_rows, clones_rows):
                  phone_number = utils.parse_phone(phone_row[0])
                  clone = clones_row[0]

                  print(Style.BRIGHT + Fore.GREEN + f"Cloning from {phone_number}")
                  app = Client(f'sessions/{phone_number}', api_id, api_hash,phone_number=phone_number)
                  app.start()

                  time.sleep(0)
                  

                  try:
                      userh = app.get_users(clone)
                      raju = app.get_chat(clone)
                      print(raju)
                      bio = raju.bio
                      print(bio)
                      if bio == None:
                         app.update_profile(bio='')
                      else:
                         app.update_profile(bio=bio)
                      firstname = userh.first_name
                      print(firstname)
                      if firstname == None:
                         app.update_profile(first_name='')
                      else:
                         app.update_profile(first_name=firstname)
                      lastname = userh.last_name
                      print(lastname)
                      if lastname == None:
                         app.update_profile(last_name='')
                      else:
                         app.update_profile(last_name=lastname)
                         
                      photos = [p for p in app.get_chat_photos("me")]
                      if photos:
                         app.delete_profile_photos(photos[0].file_id)
                         app.delete_profile_photos([p.file_id for p in photos[1:]])
                      else:
                         time.sleep(0)
                      user = app.get_users(clone)
                      peer = app.resolve_peer(user.id)
                      offset = 0  # Start fetching from the first photo
                      result = app.invoke(
                          functions.photos.GetUserPhotos(
                          user_id=peer,
                          offset=offset,
                          max_id=0,
                          limit=0
                          )
                      )

                      photos = [types.Photo._parse(app, photo) for photo in result.photos]

                      if photos:
                          for idx, photo in enumerate(photos):
        # Save the photo to a local file
                              photo_path = f'photo_{idx}.jpg'
                              app.download_media(photo, file_name=photo_path)
                              print(f'Saved photo as: {photo_path}')

                              app.invoke(functions.photos.UploadProfilePhoto(file=app.save_file(f'downloads/{photo_path}')))
                                  #app.set_profile_photo(photo=f'downloads/{photo_path}')
                              os.remove(f'downloads/{photo_path}')
                  except Exception as e:
                      print(f"Error in Clone: {str(e)}")

                  app.stop()
                  print()

          print(Style.BRIGHT + Fore.RESET + 'All Clone Done!')

# Call the function with the paths to your phone.csv and messages.csv files
     send_clones_from_csv('phone.csv', 'clone.csv')

def anonychatter():

    people = '@chatbot'
    msg1 = 'Hii'
    msg2 = 'How are you ?'
    msg3 = 'I am Girl & You?'
    msg4 = 'Can you help me'
    msg5 = 'Please'
    choice = str('/next')
    choicess = str(input('Enter Your custom Message:  '))
    numruns = int(input('How many times you want to run: '))
    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            num_runs = numruns
            run_count = 0
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            while run_count < num_runs:
                app.send_message(people,choice)
                time.sleep(3)
                app.send_message(people,msg1)
                time.sleep(3)
                app.send_message(people,msg2)
                time.sleep(4)
                app.send_message(people,msg3)
                time.sleep(5)
                app.send_message(people,msg4)
                time.sleep(6)
                app.send_message(people,msg5)
                time.sleep(3)
                app.send_message(people,choicess)
                time.sleep(2)
                run_count += 1
                print(f"Run {run_count} completed.")
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def changeraccount():

    print('Send First Name:  ')
    firstname = str(input())
    print('Send Last Name:  ')
    lastname = str(input())
    print('Send Bio Text:  ')
    bio = str(input())
    print('Enter Delay Time Per Request 0 For None: ')
    HackingZone_dev = int(input())
    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Using {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            app.update_profile(first_name=firstname, last_name=lastname, bio=bio)
            print(f'Successfull Set First, Last & Bio from {phone}')
            app.stop()
            time.sleep(HackingZone_dev)
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Login Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def changerusername():

     def send_usernames_from_csv(phone_csv_path, usernames_csv_path):
          with open(phone_csv_path, 'r') as phone_file, open(usernames_csv_path, 'r') as usernames_file:
              phone_reader = csv.reader(phone_file)
              usernames_reader = csv.reader(usernames_file)
        
              phone_rows = list(phone_reader)
              usernames_rows = list(usernames_reader)

              if len(phone_rows) != len(usernames_rows):
                  print("Error: The number of rows in 'phone.csv' and 'username.csv' is not equal.")
                  return

              for phone_row, usernames_row in zip(phone_rows, usernames_rows):
                  phone_number = utils.parse_phone(phone_row[0])
                  username = usernames_row[0]

                  print(Style.BRIGHT + Fore.GREEN + f"Changing username from {phone_number}")
                  app = Client(f'sessions/{phone_number}', api_id, api_hash,phone_number=phone_number)
                  app.start()

                  time.sleep(0)
                  

                  try:
                     app.set_username(username)
                  except Exception as e:
                      print(f"Error in Clone: {str(e)}")

                  app.stop()
                  print()

          print(Style.BRIGHT + Fore.RESET + 'All Username Done!')

# Call the function with the paths to your phone.csv and messages.csv files
     send_usernames_from_csv('phone.csv', 'username.csv')

def setprofilepic():
    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())
    print(f'{gr}Make Sure you replace opthree.jpg file')
    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Using {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            app.invoke(functions.photos.UploadProfilePhoto(file=app.save_file(f'opthree.jpg')))
            print(f'Successfull Set Profile Pic from {phone}')
            app.stop()
            time.sleep(HackingZone_dev)
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Login Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def removeprofilepic():
    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())
    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Using {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            photos = [p for p in app.get_chat_photos("me")]
            if photos:
               app.delete_profile_photos(photos[0].file_id)
               app.delete_profile_photos([p.file_id for p in photos[1:]])
            else:
               time.sleep(0)
            print(f'Successfull Removed Profile Pic from {phone}')
            app.stop()
            time.sleep(HackingZone_dev)
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Login Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def reportreasonfake():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonFake(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')

def reportreasonspam():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonSpam(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')

def reportreasonviolence():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonViolence(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')

def reportreasonchildabuse():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonChildAbuse(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')

def reportreasoncopyright():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))
    
    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()
         
    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonCopyright(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')

def reportreasongeoIrrelevant():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonGeoIrrelevant(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')


def reportreasonpersonaldetails():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonPersonalDetails(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')

def reportreasonillegaldrugs():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonIllegalDrugs(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')

def reportreasonpornography():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonPornography(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')

def reportreasonothers():
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Channel link: "))
    postid= int(input("Give post id to report: "))
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    lowercase_input = my_group.lower()

    restricted_channels = ['the_hacking_zone', '@the_hacking_zone', '@techno_trickop', '@teamtrickyabhi', '@the_hacking_zone_group', 'techno_trickop', 'teamtrickyabhi', 'the_hacking_zone_group', '1561952101', '-1001561952101', '1001561952101', 'https://t.me/the_hacking_zone_group', 'https://t.me/the_hacking_zone', '1705557435', '-1001705557435', '1001705557435', 'https://t.me/teamtrickyabhi', '1717626647', '-1001717626647', '1001717626647', 'https://t.me/techno_trickop', '1366063062', '1001366063062', '-1001366063062']

    if lowercase_input in restricted_channels:
         print('Sorry, you cannot report this channel')
         exit()

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
                
            try:
                my_id = await app.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                peer = await app.resolve_peer(my_id.id)
                result = await app.invoke(
                    functions.messages.Report(
                    peer=peer,
                    id=[postid],
                    reason=types.InputReportReasonOther(),
                    message=messages
                ))
                print(result)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')

def sendscamreport():

    scam = '@notoscam'
    config = configparser.ConfigParser()
    config.read("config.ini")
    num_messages = 1
    delay_seconds = int(input("Delay in seconds between each report: "))

    message_list = []
    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        message_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages in multimessages.csv. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:

            for i in range(num_messages):
                messages = message_row[i % len(message_row)]

                print(f"Sending report {i+1}/{num_messages} using phone number {phone}...")
                try:
                    result = await app.send_message(scam, messages)
                    print(result)

                    time.sleep(delay_seconds)
                     
                except FloodWait as e:
                    print(f'FloodWait of {e.value}')
                            
                except PeerFlood as e:
                    print(f'PeerFloodError of {e.value}')
                

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')


def fullscraper():

    search_filter = ['','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','L','M','N','O','P',
                'Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0','@','$','_','(',')','*','!','[',']']


    config = configparser.ConfigParser()
    config.read("config.ini")
    link1 = (config['HackingZone']['FromGroup']).strip()
    links= link1.split(',')
    API_ID = (config['HackingZone']['api_id']).strip()
    HashID = (config['HackingZone']['api_hash']).strip()
    my_group = config['HackingZone']['ToGroup']
    
    HackingZone_devinput = int(1)
    
    with open('phone.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        row_number = HackingZone_devinput
        col_number = 1
        value = list_of_rows[row_number - 1][col_number - 1]
        
    phone = value
    
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    if not os.path.exists(f'data.csv'):
        fp = open('data.csv', 'x')
        fp.close()

    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
        
    logging.basicConfig(level=logging.WARNING)
    def save_data(users):
        with open('data.csv', 'w', encoding="utf-8", newline='') as f:
            write = csv.writer(f)
            write.writerow(['user_id', 'first_name', 'last_name', 'username'])
            for user in users:
                user_id = user[2]
                first_name = user[3]
                last_name = user[4]
                username = user[1]
                write.writerow([user_id, first_name, last_name, username])


    def check_users(users):
        for i in range(len(users)-1,0,-1):
            user = users[i]
            if not bool(user[1]):
                del users[i]
        save_data(users)

    def update(data=[],mode='a'):
        f=open("data.csv",mode,encoding='UTF-8')   
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(data)
        f.close()
    def validate_data():
        users = []
        with open('data.csv' , 'r' , encoding='utf-8') as f:
            users1=csv.reader(f)
            users=[i for i in users1]
        check_users(users)

    user_name_list = []

    update(['user_id', 'first_name', 'last_name', 'username'],mode='w')

    link = links[0]
    old_link = link
    count = 1
    client = Client(f"sessions/{phone}", API_ID, HashID, phone_number=phone)
    client.start()
    try:
        if client.get_me():
            ans = 1
        
            try:
                client.join_chat(link)
                client.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                pass
            try:
                targetgroup = client.get_chat(link)
                my_id = client.get_chat(my_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
            existing_members = set()
            my_participants = []
            try:
               my_participants = client.get_chat_members(my_id.id)
            except Exception as e:
               print('Failed:', e)
            for rajr in my_participants:
                 existing_members.add(rajr.user.id)
            for search in search_filter:
            #print('Working Please Wait...',end='\r')
                all_participants = []
                try:
                    if bool(search):
                        all_participants = client.get_chat_members(targetgroup.id, query=search)
                    else:
                        all_participants = client.get_chat_members(targetgroup.id)
                except Exception as e:
                    print('Failed:', e)
                    input()
                    exit()
                try:
                    for user in all_participants:
                      if user.user.id not in existing_members:
                        if str(ans) == '1':
                            if not bool(user.user.username):
                                continue
                        if user.user.username in user_name_list:
                            continue
                        user_name_list.append(user.user.username)
                        if user.user.username:
                            username= user.user.username
                        else:
                            username = ""
                        if user.user.first_name:
                            firstname= user.user.first_name
                        else:
                            firstname = "NONE"
                        if user.user.last_name:
                            lastname= user.user.last_name
                        else:
                            lastname = "NONE"
                        update([user.user.id,firstname,lastname,username])
                        count += 1
					
                        print(f'Member Count : {count}',end='\r')
                except Exception as e:
                    pass
        else:
            print('Login Fail')
            input()
            exit()
        client.stop()
        print(f'Count : {count}')
        print(Style.BRIGHT + Fore.GREEN + "Task completed")
        print(Style.BRIGHT + Fore.RESET + "Enter any key to exit")
    except:
        print('Please change the config number')
        client.stop()
    input()

def sunguleadder():
    config = configparser.ConfigParser()
    config.read("config.ini")
    grouplink = config['HackingZone']['ToGroup']
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']


    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())

    phone = []

    with open('phone.csv', 'r') as delta_obj:
            csv_reader = reader(delta_obj)
            list_of_phone = tuple(csv_reader)
            for phone_ in list_of_phone:
                phone.append(int(phone_[0]))
            pphone = phone

    print(f'{gr}Total account: {n} {r}{str(len(phone))}{n}')
 
    From = int(stacno) - 1
    Upto = int(endacno)

    async def mainn():
        a = 0
        indexx = 0
        
        for xd in pphone[From:Upto]:
            
            indexx += 1
            print(f'Index : {indexx}')
            phone = utils.parse_phone(xd)
            print(f"Login {phone}")
            async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone) as app:
            
                try:
                #await app.join_chat(groupset)
                     await app.join_chat(grouplink)
                except UserAlreadyParticipant:
                     time.sleep(0)
                try:
                     my_id = await app.get_chat(grouplink)
                #TARGET = await app.get_chat(groupset)
                except Exception as e:
                     print('Failed to get chat entity:', e)
                     return
                
                nu =1
                stop = 0
                flood = 0
                added =0
                peer = 0
                userbanned = 0
                
                contacts = await app.get_contacts()
                user_to_add = []
                for contact in contacts:
                    user_to_add.append(contact.id)
                countcon = len(user_to_add)
                print(f'Total Contact in this Number: {countcon}')
                batchcount = 0
                lol = 0
                while batchcount < countcon:
                        if stop == 50:
                            print('added 50 members bracking')
                            break
                        if flood ==5:
                            print('flood errors bracking')
                            print('total added user ===',added)
                            break
                        if peer ==5:
                            print('peer flood errors bracking')
                            print('total added user ===',added)
                            break
                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total added user ===', added)
                            break
                            
                        semen = [user_to_add[batchcount]]
                        try:
                            await app.add_chat_members(my_id.id,semen)
                            print("user added", semen)
                            stop = stop +1
                            added = added +1
                            time.sleep(HackingZone_dev)
                        except FloodWait as e:
                            print(f'FloodWait of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            flood = flood + 1
                            
                        except PeerFlood as e:
                            print(f'PeerFloodError of {e.value}', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            peer = peer + 1
                            
                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            userbanned = userbanned + 1
                            
                        except UserPrivacyRestricted as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                        except UserChannelsTooMuch as e:
                    
                            await asyncio.sleep(random.randint(2,3))
                            
                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')
                        batchcount += 1
            a += 1
    asyncio.run(mainn())                  

def adderrr():

    config = configparser.ConfigParser()
    config.read("config.ini")
    groupset = config['HackingZone']['fromgroup']
    grouplink = config['HackingZone']['ToGroup']
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']

    print(Style.BRIGHT + Fore.YELLOW + 'Which Account You Want To Use?\n\nEnter: ')
    HackingZone_devinput = int(input())


    with open('phone.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        row_number = HackingZone_devinput
        col_number = 1
        value = list_of_rows[row_number - 1][col_number - 1]
        
    pphone = value

    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())
 
    From = int(stacno) - 1
    Upto = int(endacno)

    async def mainn():
        added_members = 0
        with open('done.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for roww in reader:
                if len(roww) > 0:

                    added_members = int(roww[0])
        a = 0
        added_member = added_members 
        
        if pphone:
            
            phone = utils.parse_phone(pphone)
            print(f"Login {pphone}")
            async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=pphone) as app:
            
                try:
                #await app.join_chat(groupset)
                     await app.join_chat(grouplink)
                except UserAlreadyParticipant:
                     time.sleep(0)
                try:
                     my_id = await app.get_chat(grouplink)
                #TARGET = await app.get_chat(groupset)
                except Exception as e:
                     print('Failed to get chat entity:', e)
                     return
                
                nu =1
                stop = 0
                flood = 0
                added =0
                peer = 0
                userbanned = 0
                
                with open(f'users/{phone}.csv', mode='r', encoding='UTF-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for i, row in enumerate(csv_reader):

                        with open('done.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for roww in reader:
                                if len(roww) > 0:
                                    added_members = int(roww[0])

                        with open("done.csv", mode='w', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow([added_member+1])
                        if i < added_members:
                            continue
                        if stop == 50:
                            print('added 50 members bracking')
                            break
                        if flood ==5:
                            print('flood errors bracking')
                            print('total added user ===',added)
                            break
                        if peer ==5:
                            print('peer flood errors bracking')
                            print('total added user ===',added)
                            break
                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total added user ===', added)
                            break
                            
                        user_id = await app.resolve_peer(row['user_id'])
                        try:
                            added_member += 1
                            access_hash = user_id.access_hash
                            
                            await app.add_chat_members(my_id.id,int(user_id.user_id),access_hash)
                            print("user added",row['first_name'],row['last_name'])
                            stop = stop +1
                            added = added +1
                            time.sleep(HackingZone_dev)
                        except FloodWait as e:
                            print(f'FloodWait of {e.value}', nu)
                            await asyncio.sleep(HackingZone_dev)
                            nu = nu + 1
                            flood = flood + 1
                            
                        except PeerFlood as e:
                            print(f'PeerFloodError of {e.value}', nu)
                            await asyncio.sleep(HackingZone_dev)
                            nu = nu + 1
                            peer = peer + 1
                            
                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(HackingZone_dev)
                            nu = nu + 1
                            userbanned = userbanned + 1
                            
                        except UserPrivacyRestricted as e:
                    
                            await asyncio.sleep(HackingZone_dev)
                        except UserChannelsTooMuch as e:
                    
                            await asyncio.sleep(HackingZone_dev)
                            
                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')

            a += 1
        else:
           print(f"There is no number on {HackingZone_devinput} row'")
    asyncio.run(mainn())                  


def singlefilteradderrr():

    config = configparser.ConfigParser()
    config.read("config.ini")
    groupset = config['HackingZone']['fromgroup']
    grouplink = config['HackingZone']['ToGroup']
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']

    print(Style.BRIGHT + Fore.YELLOW + 'Which Account You Want To Use?\n\nEnter: ')
    HackingZone_devinput = int(input())


    with open('phone.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        row_number = HackingZone_devinput
        col_number = 1
        value = list_of_rows[row_number - 1][col_number - 1]
        
    pphone = value

    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())
 
    From = int(stacno) - 1
    Upto = int(endacno)

    async def mainn():
        added_members = 0
        with open('done.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for roww in reader:
                if len(roww) > 0:

                    added_members = int(roww[0])
        a = 0
        added_member = added_members 
        
        if pphone:
            
            phone = utils.parse_phone(pphone)
            print(f"Login {pphone}")
            async with Client(f'sessions/{phone}', api_id, api_hash,phone_number=pphone) as app:
            
                try:
                #await app.join_chat(groupset)
                     await app.join_chat(grouplink)
                except UserAlreadyParticipant:
                     time.sleep(0)
                try:
                     my_id = await app.get_chat(grouplink)
                #TARGET = await app.get_chat(groupset)
                except Exception as e:
                     print('Failed to get chat entity:', e)
                     return
                
                nu =1
                stop = 0
                flood = 0
                added =0
                peer = 0
                userbanned = 0
                
                with open(f'users/{phone}.csv', mode='r', encoding='UTF-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for i, row in enumerate(csv_reader):

                        with open('done.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for roww in reader:
                                if len(roww) > 0:
                                    added_members = int(roww[0])

                        with open("done.csv", mode='w', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow([added_member+1])
                        if i < added_members:
                            continue
                        if stop == 50:
                            print('added 50 members bracking')
                            break
                        if flood ==5:
                            print('flood errors bracking')
                            print('total added user ===',added)
                            break
                        if peer ==5:
                            print('peer flood errors bracking')
                            print('total added user ===',added)
                            break
                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total added user ===', added)
                            break
                            
                        username = row['username']
                        try:
                            added_member += 1
                            await app.add_chat_members(my_id.id,str(username))
                            print("user added",row['first_name'],row['last_name'])
                            stop = stop +1
                            added = added +1
                            time.sleep(HackingZone_dev)
                        except FloodWait as e:
                            print(f'FloodWait of {e.value}', nu)
                            await asyncio.sleep(HackingZone_dev)
                            nu = nu + 1
                            flood = flood + 1
                            
                        except PeerFlood as e:
                            print(f'PeerFloodError of {e.value}', nu)
                            await asyncio.sleep(HackingZone_dev)
                            nu = nu + 1
                            peer = peer + 1
                            
                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(HackingZone_dev)
                            nu = nu + 1
                            userbanned = userbanned + 1
                            
                        except UserPrivacyRestricted as e:
                    
                            await asyncio.sleep(HackingZone_dev)
                        except UserChannelsTooMuch as e:
                    
                            await asyncio.sleep(HackingZone_dev)
                            
                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')

            a += 1
        else:
           print(f"There is no number on {HackingZone_devinput} row'")
    asyncio.run(mainn())                  

def deletealreadyfilter():

    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    #print(f'Total account: {str(len(phone))}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Filtering From {phone}")
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
            except UserAlreadyParticipant:
                time.sleep(1)
            my_id = await app.get_chat(my_group)
            existing_members = set()
            filtered_rows = []
            async for mygroupmembers in app.get_chat_members(chat_id=my_id.id):
                existing_members.add(mygroupmembers.user.id)
            with open('data.csv', 'r', newline='', encoding='UTF-8') as input_file:
                  csv_reader = csv.DictReader(input_file)
    
                  for row in csv_reader:
                        user_id = int(row['user_id'])
                        if user_id not in existing_members:
                              filtered_rows.append(row)
            os.remove("data.csv")
            with open('data.csv', 'w', newline='', encoding='UTF-8') as output_file:
                  fieldnames = ['user_id', 'first_name', 'last_name', 'username']
                  csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
                  csv_writer.writeheader()
    
                  csv_writer.writerows(filtered_rows)

            print("Filtered data has been saved to data.csv")
   
    async def scrape_all():
        batch_size = 1  # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())

def viewsincreaser():

    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            my_id = app.get_chat("@hdjdhhdndnxud")
            peer = app.resolve_peer(my_id.id)
            result = app.invoke(
                 functions.messages.GetMessagesViews(
                 peer=peer,
                 id=[26],
                 increment=True
            ))
            print(result)
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Login Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def premiumscraper():

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = config['HackingZone']['ToGroup']
    TARGET_group = config['HackingZone']['fromgroup']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    if os.path.exists(f'done.csv'):
        os.remove(f'done.csv')
    if not os.path.exists(f'done.csv'):
        fp = open('done.csv', 'x')
        fp.close()
    if os.path.exists(f'data.csv'):
        os.remove(f'data.csv')
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    async def mainn(xd):
        phone = utils.parse_phone(xd)
        
        print(f"Scraping from {phone}")
        
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(my_group)
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(0)
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_id = await app.get_chat(my_group)
                TARGET = await app.get_chat(TARGET_group)
            except Exception as e:
                print('Failed to get chat entity:', e)
                return

            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                
                existing_members = set()
                
                async for my_group_member in app.get_chat_members(chat_id=my_id.id):
                    existing_members.add(my_group_member.user.id)
                    
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
                    if targetMember.user.id not in existing_members:
                    
                        user_id = targetMember.user.id
                        first_name = targetMember.user.first_name or ''
                        last_name = targetMember.user.last_name or ''
                        username = targetMember.user.username or ''
                        status = None
                        if username:
                        # Check if the member is online or seen recently before saving
                            try:
                                entity = await app.get_users(targetMember.user.id)
                                if entity.is_premium:
                                    status = 'Premium'
                            except Exception as e:
                                print('Failed to get entity or status:', e)
                            

                            if status:
                                writer.writerow({'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'username': username, 'status': status})
                                print("User saved:", first_name, "Status:", status)
                        else:
                            time.sleep(0)

        print('All members saved for', phone)
    async def scrape_all():
        batch_size = 1 # Number of accounts to process in each batch
        total_accounts = 1

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())


def hidelastseen():

    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            app.invoke(functions.account.SetPrivacy(key=types.InputPrivacyKeyStatusTimestamp(), rules=[types.InputPrivacyValueDisallowAll()]))
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Hide Last Seen Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to Exit')
    input()

def hidenumbersp():

    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            app.invoke(functions.account.SetPrivacy(key=types.InputPrivacyKeyPhoneNumber(), rules=[types.InputPrivacyValueDisallowAll()]))
            app.invoke(functions.account.SetPrivacy(key=types.InputPrivacyKeyAddedByPhone(), rules=[types.InputPrivacyValueAllowContacts()]))
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Hide Numbers Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()


def hidenmbandphone():

    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            print("Hiding Last Seen")
            app.invoke(functions.account.SetPrivacy(key=types.InputPrivacyKeyStatusTimestamp(), rules=[types.InputPrivacyValueDisallowAll()]))
            print("Hiding Number")
            app.invoke(functions.account.SetPrivacy(key=types.InputPrivacyKeyPhoneNumber(), rules=[types.InputPrivacyValueDisallowAll()]))
            app.invoke(functions.account.SetPrivacy(key=types.InputPrivacyKeyAddedByPhone(), rules=[types.InputPrivacyValueAllowContacts()]))
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Hide Last Seen and Phone Number Hide Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()

def randomusernameh():

    with open('phone.csv', 'r')as f:
        str_list = [row[0] for row in csv.reader(f)]
        po = 0
        for pphone in str_list:
            phone = utils.parse_phone(pphone)
            po += 1
            print(Style.BRIGHT + Fore.GREEN + f"Login {phone}")
            app = Client(f'sessions/{phone}', api_id, api_hash,phone_number=phone)
            app.start()
            username = None
            while not username:
                username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
                try:
                    print(f"Setting Username: {username}")
                    app.set_username(username)
                except:
                    print(f'Username {username} is already occupied, generating a new one.')
                    username = None
            app.stop()
            print()
        done = True
    print(Style.BRIGHT + Fore.RESET + 'All Number Random Username Done !' if done else "Error!")
    print(Style.BRIGHT + Fore.YELLOW + 'Press Enter to back')
    input()
    
def rmfour():

    file_path = "ramexfour.py"
    if os.path.exists(file_path):
        print(f"{re}RamexFour file detected Executing {gr}{file_path} ...")
        time.sleep(2)
        os.system(f"{sys.executable} {file_path}")
    else:
        print(f"{re}File {gr}{file_path} missing. Download and extract again.")


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        
def main_menu():
    clr()
    banner()
    print(f'{Style.BRIGHT + Fore.CYAN + Back.RED}[+] {gr}Main Options:'+n)
    print(f'{Style.BRIGHT + Fore.GREEN}[1] Login'+n)
    print(f'{Style.BRIGHT + Fore.GREEN}[2] Member Adder'+n)
    print(f'{Style.BRIGHT + Fore.GREEN}[3] Subscribe To TrickyAbhi'+n)
    print(f'{Style.BRIGHT + Fore.GREEN}[4] Scraper'+n)
    print(f'{Style.BRIGHT + Fore.GREEN}[5] Adder'+n)
    print(f'{Style.BRIGHT + Fore.GREEN}[6] Private Scraper'+n)
    print(f'{Style.BRIGHT + Fore.GREEN}[7] Private Group Adder'+n)
    print(f'{Style.BRIGHT + Fore.GREEN}[8] Multi Account Adding (Multi Threading)'+n)
    print(f'{Style.BRIGHT + Fore.CYAN + Back.RED}[+] {gr}Filter & Filter Adder Options (Updated):'+n)
    print(f'{Style.BRIGHT + Fore.RED}[9] Scraper (Not Recommended - Use Only if you have more than 50k+ members)'+n)
    print(f'{Style.BRIGHT + Fore.RED}[10] Hidden Members Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[11] Private Hidden Members Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[12] Daily Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[13] Private Daily Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[14] Weekly Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[15] Private Weekly Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[16] Monthly Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[17] Private Monthly Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[18] Inactive Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[19] Private Inactive Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[20] Online Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[21] Private Online Filter Scraper'+n)
    print(f'{Style.BRIGHT + Fore.RED}[22] Filter Adder {gr}(Updated this August) [Only for option 9 to 21 and option 43]'+n)
    print(f'{Style.BRIGHT + Fore.CYAN + Back.RED}[+] {gr}Contact Adder Options:'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[23] Contact Adder'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[24] Contact Deleter'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[25] Bulk Adder (first use option 20)'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[26] Multi Threading Bulk Adder (first use option 20)'+n)
    print(f'{Style.BRIGHT + Fore.CYAN + Back.RED}[+] {gr}Other Options:'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[27] Ban Filter + Remover'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[28] Permanent Limit Remover v1'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[29] Permanent Limit Remover v2'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[30] OTP Viewer'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[31] Group/Channel Joiner'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[32] Group/Channel Lefter'+n)
    print(f'{Style.BRIGHT + Fore.CYAN + Back.RED}[+] {gr}New Options:'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[33] Reaction Increaser'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[34] Shares Increaser'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[35] Mass DM'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[36] Account Cloner'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[37] Anony Chatter'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[38] Set First, Last Name & Bio Changer'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[39] Set Username'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[40] Set Profile Pic'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[41] Remove Profile Pic'+n)
    print(f'{Style.BRIGHT + Fore.RED + Back.GREEN}[42] Reporter (Now for Everyone)'+n)
    print(f'{Style.BRIGHT + Fore.CYAN + Back.RED}[+] {gr}Extra Options:'+n)
    print(f'{Style.BRIGHT + Fore.RED}[43] Full Scraper - {gr}(After Scrape Add using option 22)'+n)
    print(f'{Style.BRIGHT + Fore.RED}[44] Adder using Contact - {gr}(First use option 23)'+n)
    print(f'{Style.BRIGHT + Fore.RED}[45] Single Adder - {gr}(Adding using Single Account)'+n)
    print(f'{Style.BRIGHT + Fore.RED}[46] Single Filter Adder - {gr}(Only for option 9 to 21 and 43 option)'+n)
    print(f'{Style.BRIGHT + Fore.RED}[47] Delete Already Filter - {gr}(Only for option 9 to 21 and 43 option)'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[48] Premium Members Scraper'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[49] Hide Last Seen'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[50] Hide Phone Numbers'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[51] Hide Last Seen & Numbers Both'+n)
    print(f'{Style.BRIGHT + Fore.WHITE}[52] Set Random Username'+n)
    print(f'{Style.BRIGHT + Fore.YELLOW}[53] Go Back'+n)
    print(f'{Style.BRIGHT + Fore.YELLOW}[54] Exit'+n)
    a = int(input('\nEnter your choice: '))
    if a == 1:
        login()
    elif a == 2:
        directadder()    
    elif a == 3:
        # thanks to github.com/th3unkn0n for the snippet below
        url = 'https://youtube.com/@TrickyAbhi2.0'
        brw = 'am start --user 0 -a android.intent.action.VIEW -d %s'
        cmd = brw % url
        os.system(cmd)
        print('opened by command:', repr(cmd), end='\n\n')
    elif a == 4:
        scraper()
    elif a == 5:
        adder()
    elif a == 6:
        pvtscraper()
    elif a == 7:
        pvtadder()
    elif a == 8:
        MultiAdderFunction()
    elif a == 9:
        multi_ccraper()
    elif a == 10:
        hiddenscraper()
    elif a == 11:
        pvthiddenscraper()
    elif a == 12:
        dailyfilter()
    elif a == 13:
        pvtdailyfilter()
    elif a == 14:
        weeklyfilter()
    elif a == 15:
        pvtweeklyfilter()
    elif a == 16:
        monthlyfilter()
    elif a == 17:
        pvtmonthlyfilter()
    elif a == 18:
        inactivefilter()
    elif a == 19:
        pvtinactivefilter()
    elif a == 20:
        onlinefilter()
    elif a == 21:
        pvtonlinefilter()
    elif a == 22:
        filterwalaadder()
    elif a == 23:
        contactadder()
    elif a == 24:
        contactdeleter()
    elif a == 25:
        bulkadder()
    elif a == 26:
        bulkaddermulti()
    elif a == 27:
        BanFilter()
    elif a == 28:
        permanentlimitremover()
    elif a == 29:
        permanentlimitremover2()
    elif a == 30:
        otpviewer()
    elif a == 31:
        groupjoiner()
    elif a == 32:
        grouplefter()
    elif a == 33:
        reactionincreaser()
    elif a == 34:
        sharesincreaser()
    elif a == 35:
        massdm()
    elif a == 36:
        autoidcloner()
    elif a == 37:
        anonychatter()
    elif a == 38:
        changeraccount()
    elif a == 39:
        changerusername()
    elif a == 40:
        setprofilepic()
    elif a == 41:
        removeprofilepic()
    elif a == 42:
        reporterbytgreport()
    elif a == 43:
        fullscraper()
    elif a == 44:
        sunguleadder()
    elif a == 45:
        adderrr()
    elif a == 46:
        singlefilteradderrr()()
    elif a == 47:
        deletealreadyfilter()
    elif a == 48:
        premiumscraper()
    elif a == 49:
        hidelastseen()
    elif a == 50:
        hidenumbersp()
    elif a == 51:
        hidenmbandphone()
    elif a == 52:
        randomusernameh()
    elif a == 53:
        rmfour()
    elif a == 54:
        exit()
        
   
#main_menu()

def reporterbytgreport():
    clr()
    banner()
    print(f'{Style.BRIGHT + Fore.YELLOW + Back.RED}[+] Report Channel Post Option (with Messages):'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[1] Report Fake'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[2] Report Spam'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[3] Report Violence'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[4] Report Child Abuse'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[5] Report Copyright'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[6] Report GeoIrrelevant'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[7] Report Personal Details'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[8] Report Illegal drugs'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[9] Report Pornography'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[10] Report Others'+n)
    print(f'{Style.BRIGHT + Fore.YELLOW + Back.RED}[+] Exit Option:'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[0] Go Back'+n)
    print(f'{Style.BRIGHT + Fore.CYAN}[11] Exit'+n)
    b = int(input('\nEnter your choice: '))
    if b == 1:
        reportreasonfake()
    elif b == 2:
        reportreasonspam()
    elif b == 3:
        reportreasonviolence()
    elif b == 4:
        reportreasonchildabuse()
    elif b == 5:
        reportreasoncopyright()
    elif b == 6:
        reportreasongeoIrrelevant()
    elif b == 7:
        reportreasonpersonaldetails()
    elif b == 8:
        reportreasonillegaldrugs()
    elif b == 9:
        reportreasonpornography()
    elif b == 10:
        reportreasonothers()
    elif b == 0:
        main_menu()
    elif b == 11:
        exit()

main_menu()