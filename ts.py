import sys
import pickle, os
from time import sleep
import webbrowser
import time
import random
import pyfiglet
import names
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
import datetime
from pyrogram import types
from pyrogram.raw import functions, types
from pyrogram.enums import UserStatus
from pyrogram.errors import UserDeactivated, AuthKeyUnregistered, SessionExpired, UserDeactivatedBan
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

config = configparser.ConfigParser()
config.read("config.ini")
changableapi = config['HackingZone']['api_id']
changablehash = config['HackingZone']['api_hash']


API_ID = int(changableapi)
HashID = str(changablehash)

def messagesendergroup():

    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = my_group = str(input("Send Group link: "))
    num_messages = int(input("How many ads you want to send? "))
    delay_seconds = int(input("Delay in seconds between per ads? "))
        
        
    with open('message.csv', 'r') as f:
        message_list = [row[0] for row in csv.reader(f)]
        
        
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

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                 await client.join_chat(my_group)
            except UserAlreadyParticipant:
                 pass
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_group_entity = await client.get_chat(my_group)
            except Exception as e:
                print('Failed to connect:', e)
                return
            async def send_message(phone, message):
                 await client.send_message(my_group_entity.id, message)
                 
            for i in range(num_messages):
            
                message = message_list[i % len(message_list)]

                print(f"Sending message {i+1}/{num_messages} to {my_group} using phone number {phone}...")

                await send_message(phone, message)

                time.sleep(delay_seconds)
    async def scrape_all():
        batch_size = 8  # Number of accounts to process in each batch
        total_accounts = len(pphone)

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i+batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())
    print('All Accounts Done')
    
def messagesendergrouppic():

    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Group link: "))
    num_messages = int(input("How many ads you want to send? "))
    #num_messages = 5
    delay_seconds = int(input("Delay in seconds between per ads? "))
    #delay_seconds = 0
    picpath = str(input("Enter Image Name with extension: "))

    with open('message.csv', 'r') as f:
        message_list = [row[0] for row in csv.reader(f)]

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

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                 await client.join_chat(my_group)
            except UserAlreadyParticipant:
                 pass
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_group_entity = await client.get_chat(my_group)
            except Exception as e:
                print('Failed to connect:', e)
                return

            async def send_message(phone, caption, image_path):
                await client.send_photo(my_group_entity.id, picpath, caption=caption)

            for i in range(num_messages):
                caption = message_list[i % len(message_list)]
                image_path = picpath  # Replace with the actual image path

                print(f"Sending message {i+1}/{num_messages} to {my_group} using phone number {phone}...")

                await send_message(phone, caption, image_path)

                time.sleep(delay_seconds)

    async def scrape_all():
        batch_size = 8  # Number of accounts to process in each batch
        total_accounts = len(pphone)

        for i in range(0, total_accounts, batch_size):
            batch = pphone[i:i + batch_size]
            tasks = [mainn(xd) for xd in batch]
            await asyncio.gather(*tasks)

    asyncio.run(scrape_all())
    print('All Accounts Done')
    
def messagesendergrouppicsingle():

    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Group link: "))
    num_messages = int(input("How many ads you want to send? "))
    #num_messages = 5
    #delay_seconds = 0
    delay_seconds = int(input("Delay in seconds between per ads? "))
    picpath = str(input("Enter Image Name with extension: "))

    with open('message.csv', 'r') as f:
        message_list = [row[0] for row in csv.reader(f)]

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    selected_index = int(input("Which account you want to use? ")) - 1

    if selected_index < 0 or selected_index >= total_accounts:
        print("Invalid account index selected. Exiting...")
        return

    selected_phone = phone_list[selected_index][0]

    print(f'Using account: {selected_phone}')

    async def mainn(phone):
        phone = utils.parse_phone(phone)

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                 await client.join_chat(my_group)
            except UserAlreadyParticipant:
                 pass
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_group_entity = await client.get_chat(my_group)
            except Exception as e:
                print('Failed to connect:', e)
                return

            async def send_message(phone, caption, image_path):
                await client.send_photo(my_group_entity.id, picpath, caption=caption)

            for i in range(num_messages):
                caption = message_list[i % len(message_list)]
                image_path = picpath # Replace with the actual image path

                print(f"Sending message {i+1}/{num_messages} to {my_group} using phone number {phone}...")

                await send_message(phone, caption, image_path)

                time.sleep(delay_seconds)

    asyncio.run(mainn(selected_phone))
    print('Account Done')
    
def messagesendergroupsingle():

    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Group link: "))
    num_messages = int(input("How many ads do you want to send? "))
    delay_seconds = int(input("Delay in seconds between each ad? "))

    with open('message.csv', 'r') as f:
        message_list = [row[0] for row in csv.reader(f)]

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    selected_index = int(input("Which account yiu want to use?: ")) - 1

    if selected_index < 0 or selected_index >= total_accounts:
        print("Invalid account index selected. Exiting...")
        return

    selected_phone = phone_list[selected_index][0]

    print(f'Using account: {selected_phone}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                 await client.join_chat(my_group)
            except UserAlreadyParticipant:
                 pass
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_group_entity = await client.get_chat(my_group)
            except Exception as e:
                print('Failed to connect:', e)
                return

            async def send_message(phone, message):
                await client.send_message(my_group_entity.id, message)

            for i in range(num_messages):
                message = message_list[i % len(message_list)]

                print(f"Sending message {i+1}/{num_messages} to {my_group} using phone number {phone}...")

                await send_message(phone, message)

                time.sleep(delay_seconds)

    asyncio.run(mainn(selected_phone))
    print('Account Done')
    
def messagesendergroupmultimsg():

    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Group link: "))
    num_messages = int(input("How many ads do you want to send? "))
    delay_seconds = int(input("Delay in seconds between each ad? "))

    message_list = []

    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f)
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

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                 await client.join_chat(my_group)
            except UserAlreadyParticipant:
                 pass
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_group_entity = await client.get_chat(my_group)
            except Exception as e:
                print('Failed to connect:', e)
                return

            async def send_message(phone, message):
                await client.send_message(my_group_entity.id, message)

            for i in range(num_messages):
                message = message_row[i % len(message_row)]

                print(f"Sending message {i+1}/{num_messages} to {my_group} using phone number {phone}...")

                await send_message(phone, message)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')
        
        
def messagesendergroupmultimsgpic():

    config = configparser.ConfigParser()
    config.read("config.ini")
    my_group = str(input("Send Group link: "))
    num_messages = int(input("How many ads do you want to send? "))
    delay_seconds = int(input("Delay in seconds between each ad? "))

    message_list = []
    image_list = []

    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f)
        message_list = list(csv_reader)

    with open('multiimages.csv', 'r') as f:
        csv_reader = csv.reader(f)
        image_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts or len(image_list) < total_accounts:
        print("Insufficient messages or images. Exiting...")
        return

    async def mainn(xd, message_row, image_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                 await client.join_chat(my_group)
            except UserAlreadyParticipant:
                 pass
            except Exception as e:
                print('Failed to connect:', e)
                return
            try:
                my_group_entity = await client.get_chat(my_group)
            except Exception as e:
                print('Failed to connect:', e)
                return

            async def send_message(phone, message_info, image_info):
                await client.send_photo(my_group_entity.id, image_info, caption=message_info)

            for i in range(num_messages):
                message_info = message_row[i % len(message_row)]

                image_info = image_row[i % len(image_row)]

                print(f"Sending message {i+1}/{num_messages} to {my_group} using phone number {phone}...")

                await send_message(phone, message_info, image_info)

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]
        selected_image_row = image_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row, selected_image_row))
        print('Account Done')
        
        
def messagesendergroupmultimsgpicmultigroups():
    config = configparser.ConfigParser()
    config.read("config.ini")
    num_messages = int(input("How many ads do you want to send? "))
    delay_seconds = int(input("Delay in seconds between each ad? "))

    message_list = []
    image_list = []

    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f)
        message_list = list(csv_reader)

    with open('multiimages.csv', 'r') as f:
        csv_reader = csv.reader(f)
        image_list = list(csv_reader)

    group_list = []

    with open('multigroups.csv', 'r') as f:
        csv_reader = csv.reader(f)
        group_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts or len(image_list) < total_accounts:
        print("Insufficient messages or images. Exiting...")
        return

    async def mainn(xd, message_row, image_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                for group_info in group_list:
                    group = group_info[0]
                    await client.join_chat(group.strip())
            except UserAlreadyParticipant:
                    pass
            except Exception as e:
                print('Failed to connect:', e)
                return

            async def send_message(phone, message_info, image_info, group):
                try:
                   my_group_entity = await client.get_chat(group)
                except Exception as e:
                   print('Failed to connect:', e)
                   return
                await client.send_photo(my_group_entity.id, image_info, caption=message_info)

            for i in range(num_messages):
                message_info = message_row[i % len(message_row)]

                image_info = image_row[i % len(image_row)]

                print(f"Sending message {i+1}/{num_messages} to {group_list} using phone number {phone}...")

                for group_info in group_list:
                    group = group_info[0]
                    await send_message(phone, message_info, image_info, group.strip())

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]
        selected_image_row = image_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row, selected_image_row))
        print('Account Done')
        
def messagesendergroupmultimsgmultigroups():
    config = configparser.ConfigParser()
    config.read("config.ini")
    num_messages = int(input("How many ads do you want to send? "))
    delay_seconds = int(input("Delay in seconds between each ad? "))

    message_list = []

    with open('multimessages.csv', 'r') as f:
        csv_reader = csv.reader(f)
        message_list = list(csv_reader)

    group_list = []

    with open('multigroups.csv', 'r') as f:
        csv_reader = csv.reader(f)
        group_list = list(csv_reader)

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    if len(message_list) < total_accounts:
        print("Insufficient messages or images. Exiting...")
        return

    async def mainn(xd, message_row):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                for group_info in group_list:
                    group = group_info[0]
                    await client.join_chat(group.strip())
            except UserAlreadyParticipant:
                    pass
            except Exception as e:
                print('Failed to connect:', e)
                return

            async def send_message(phone, message_info, group):
                try:
                   my_group_entity = await client.get_chat(group)
                except Exception as e:
                   print('Failed to connect:', e)
                   return
                await client.send_message(my_group_entity.id, message_info)
                
            for i in range(num_messages):
                message_info = message_row[i % len(message_row)]

                print(f"Sending message {i+1}/{num_messages} to {group_list} using phone number {phone}...")

                for group_info in group_list:
                    group = group_info[0]
                    await send_message(phone, message_info, group.strip())

                time.sleep(delay_seconds)

    for index, phone_info in enumerate(phone_list):
        selected_phone = phone_info[0]
        selected_message_row = message_list[index]

        print(f'\nUsing account: {selected_phone}')

        asyncio.run(mainn(selected_phone, selected_message_row))
        print('Account Done')
        
def messagesendermultigroupsinglepic():

    config = configparser.ConfigParser()
    config.read("config.ini")
    
    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    account_index = int(input("Which account do you want to use? ")) - 1
    image_path = str(input("Enter file name with extension: "))
    num_messages = int(input("How many ads do you want to send? "))
    delay_seconds = int(input("Delay in seconds between each ad? "))

    with open('message.csv', 'r') as f:
        csv_reader = csv.reader(f)
        message_list = list(csv_reader)
        selected_message = message_list[0][0]  # Select the first message

    group_list = []

    with open('multigroups.csv', 'r') as f:
        csv_reader = csv.reader(f)
        group_list = list(csv_reader)

    selected_phone_info = phone_list[account_index]
    selected_phone = selected_phone_info[0]

    print(f'Using account: {selected_phone}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                for group_info in group_list:
                    group = group_info[0]
                    await client.join_chat(group.strip())
            except UserAlreadyParticipant:
                    pass
            except Exception as e:
                print('Failed to connect:', e)
                return

            async def send_message(phone, message_info, image_path, group):
                try:
                   my_group_entity = await client.get_chat(group)
                except Exception as e:
                   print('Failed to connect:', e)
                   return
                await client.send_photo(my_group_entity.id, image_path, caption=message_info)

            for i in range(num_messages):
                print(f"Sending message {i+1}/{num_messages} to groups using phone number {phone}...")

                for group_info in group_list:
                    group = group_info[0]
                    await send_message(phone, selected_message, image_path, group)

                time.sleep(delay_seconds)

    asyncio.run(mainn(selected_phone))
    print('Account Done')
    
def messagesendermultigroupsingle():

    config = configparser.ConfigParser()
    config.read("config.ini")

    phone_list = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        phone_list = list(csv_reader)

    total_accounts = len(phone_list)
    print(f'Total accounts: {total_accounts}')

    for index, phone_info in enumerate(phone_list):
        print(f"{index+1}. {phone_info[0]}")

    account_index = int(input("Which account do you want to use? ")) - 1
    num_messages = int(input("How many ads do you want to send? "))
    delay_seconds = int(input("Delay in seconds between each ad? "))

    with open('message.csv', 'r') as f:
        csv_reader = csv.reader(f)
        message_list = list(csv_reader)
        selected_message = message_list[0][0]  # Select the first message

    group_list = []

    with open('multigroups.csv', 'r') as f:
        csv_reader = csv.reader(f)
        group_list = list(csv_reader)

    selected_phone_info = phone_list[account_index]
    selected_phone = selected_phone_info[0]

    print(f'Using account: {selected_phone}')

    async def mainn(xd):
        phone = utils.parse_phone(xd)

        print(f"Login {phone}")

        async with Client(f'sessions/{phone}', API_ID, HashID) as client:
            try:
                for group_info in group_list:
                    group = group_info[0]
                    await client.join_chat(group.strip())
            except UserAlreadyParticipant:
                    pass
            except Exception as e:
                print('Failed to connect:', e)
                return

            async def send_message(phone, message, group):
                try:
                   my_group_entity = await client.get_chat(group)
                except Exception as e:
                   print('Failed to connect:', e)
                   return
                await client.send_message(my_group_entity.id, message)

            for i in range(num_messages):

                print(f"Sending message {i+1}/{num_messages} to groups using phone number {phone}...")

                for group_info in group_list:
                    group = group_info[0]
                    await send_message(phone, selected_message, group)

                time.sleep(delay_seconds)

    asyncio.run(mainn(selected_phone))
    print('Account Done')
    
def forward_to_channels():

    config = configparser.ConfigParser()
    config.read("config.ini")
    phone = (config['HackingZone']['phone']).strip()
    yourchannel = str(input("If Private Give Your Channel Link, If Public Give Username: "))
    # Load the list of channels from multichannels.csv
    channel_list = []
    all_list = set()
    with open('multichannels.csv', 'r') as f:
        csv_reader = csv.reader(f)
        channel_list = list(csv_reader)
        
    client = Client(f"sessions/{phone}", API_ID, HashID)
    with client:
        try:
            for group_info in channel_list:
                group = group_info[0]
                print(group)
                client.join_chat(group.strip())
        except UserAlreadyParticipant:
            pass
        # Add an event handler to forward new messages from the source channel
        try:
            my_group_entity = client.get_chat(yourchannel)
        except Exception as e:
            print('Failed to connect:', e)
            return
        try:
            for group_infos in channel_list:
                groups = group_infos[0]
                everyone_group_entity = client.get_chat(groups.strip())
                all_list.add(everyone_group_entity.id)
        except Exception as e:
            print('Failed to connect:', e)
            return
    @client.on_message()
    async def my_handler(client, message):
            print(f'Now Try to Post in your Channel')
            if message.chat.id in all_list:
                try:
                    await message.forward(my_group_entity.id)
                    print(f"Message forwarded to {yourchannel}")
                except Exception as e:
                    print(f"Failed to forward message to {yourchannel}: {e}")
            else:
                print("Not Found")
    client.run()
    
def forward_to_channelsnotag():

    config = configparser.ConfigParser()
    config.read("config.ini")
    phone = (config['HackingZone']['phone']).strip()
    yourchannel = str(input("If Private Give Your Channel Link, If Public Give Username: "))
    # Load the list of channels from multichannels.csv
    channel_list = []
    all_list = set()
    with open('multichannels.csv', 'r') as f:
        csv_reader = csv.reader(f)
        channel_list = list(csv_reader)
        
    client = Client(f"sessions/{phone}", API_ID, HashID)
    with client:
        try:
            for group_info in channel_list:
                group = group_info[0]
                print(group)
                client.join_chat(group.strip())
        except UserAlreadyParticipant:
            pass
        # Add an event handler to forward new messages from the source channel
        try:
            my_group_entity = client.get_chat(yourchannel)
        except Exception as e:
            print('Failed to connect:', e)
            return
        try:
            for group_infos in channel_list:
                groups = group_infos[0]
                everyone_group_entity = client.get_chat(groups.strip())
                all_list.add(everyone_group_entity.id)
        except Exception as e:
            print('Failed to connect:', e)
            return
    @client.on_message()
    async def my_handler(client, message):
            print(f'Now Try to Post in your Channel')
            if message.chat.id in all_list:
                try:
                    await message.copy(my_group_entity.id)
                    print(f"Message forwarded to {yourchannel}")
                except Exception as e:
                    print(f"Failed to forward message to {yourchannel}: {e}")
            else:
                print("Not Found")
    client.run()
    
def multi_ccraper():
    config = configparser.ConfigParser()
    config.read("config.ini")
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
        
        if os.path.exists(f'data.csv'):
            os.remove(f'data.csv')
            
        async with Client(f'sessions/{phone}', api_id, api_hash, phone_number=phone) as app:
            try:
                await app.join_chat(TARGET_group)
            except UserAlreadyParticipant:
                time.sleep(1)
            TARGET = await app.get_chat(TARGET_group)
            with open(F'data.csv', encoding="UTF-8", mode='a', newline='') as csv_file:
                fieldnames = ['user_id', 'first_name', 'last_name', 'username']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                async for targetMember in app.get_chat_members(chat_id=TARGET.id):
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
    
def messagesendering():

    config = configparser.ConfigParser()
    config.read("config.ini")
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    raj = int(input("How many messages you want to send per account: "))
    
    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())
    
    with open('message.csv', 'r', newline='') as f:
        selected_message = f.read()  # Select the first message
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    print(f'Total account: {str(len(phone))}')

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

            async with Client(f'sessions/{phone}', api_id, api_hash) as client:

                nu = 1
                stop = 0
                flood = 0
                added = 0
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
                            csv_writer.writerow([added_member + 1])

                        if i < added_members:
                            continue

                        if stop == raj:
                            print(f'sent successful to {raj} members breaking')
                            break

                        if flood == 5:
                            print('flood errors breaking')
                            print('total sent user ===', added)
                            break

                        if peer == 5:
                            print('peer flood errors breaking')
                            print('total sent user ===', added)
                            break

                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total sent user ===', added)
                            break

                        username = str(row['username'])
                        #peers = PeerUser(username)
                        try:
                            added_member += 1
                            await client.send_message(username, selected_message)
                            print("Message Sent to ", row['first_name'])
                            stop = stop + 1
                            added = added + 1
                            time.sleep(HackingZone_dev)
                            
                        except UserPrivacyRestricted:
                            await asyncio.sleep(random.randint(2,3))
                            
                            
                        except UserChannelsTooMuch:
                            await asyncio.sleep(0)
                            
                        except PeerFlood as e:
                            print('PeerFloodError', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            peer = peer + 1

                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            userbanned = userbanned + 1

                        except FloodWait as e:
                            print('FloodWait', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            flood = flood + 1

                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')





                        except:
                            traceback.print_exc()
                            print(f"Unexpected Error")

            a += 1

    asyncio.run(mainn())              
    
    
def messagesenderingpic():

    config = configparser.ConfigParser()
    config.read("config.ini")
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    image_path = str(input("Enter file name with extension: "))
    
    raj = int(input("How many messages you want to send per account: "))
    
    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())
    
    with open('message.csv', 'r', newline='') as f:
        selected_message = f.read()  # Select the first message
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    print(f'Total account: {str(len(phone))}')

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

            async with Client(f'sessions/{phone}', api_id, api_hash) as client:

                nu = 1
                stop = 0
                flood = 0
                added = 0
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
                            csv_writer.writerow([added_member + 1])

                        if i < added_members:
                            continue

                        if stop == raj:
                            print(f'sent successful to {raj} members breaking')
                            break

                        if flood == 5:
                            print('flood errors breaking')
                            print('total sent user ===', added)
                            break

                        if peer == 5:
                            print('peer flood errors breaking')
                            print('total sent user ===', added)
                            break

                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total sent user ===', added)
                            break

                        username = str(row['username'])
                        #peers = PeerUser(username)
                        try:
                            added_member += 1
                            await client.send_photo(username, image_path, caption=selected_message)
                            print("Message Sent to ", row['first_name'])
                            stop = stop + 1
                            added = added + 1
                            time.sleep(HackingZone_dev)
                            
                        except UserPrivacyRestricted:
                            await asyncio.sleep(random.randint(2,3))
                            
                            
                        except UserChannelsTooMuch:
                            await asyncio.sleep(0)
                            
                        except PeerFlood as e:
                            print('PeerFloodError', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            peer = peer + 1

                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            userbanned = userbanned + 1

                        except FloodWait as e:
                            print('FloodWait', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            flood = flood + 1

                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')





                        except:
                            traceback.print_exc()
                            print(f"Unexpected Error")

            a += 1

    asyncio.run(mainn())              
    
    
def addtocontactbyimp():

    config = configparser.ConfigParser()
    config.read("config.ini")
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    raj = int(input("How many Number you want to import per account: "))
    
    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    print(f'Total account: {str(len(phone))}')

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

            async with Client(f'sessions/{phone}', api_id, api_hash) as client:

                nu = 1
                stop = 0
                flood = 0
                added = 0
                peer = 0
                userbanned = 0

                with open(f'numbers.csv', mode='r', encoding='UTF-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for i, row in enumerate(csv_reader):

                        with open('done.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for roww in reader:
                                if len(roww) > 0:
                                    added_members = int(roww[0])

                        with open("done.csv", mode='w', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow([added_member + 1])

                        if i < added_members:
                            continue

                        if stop == raj:
                            print(f'sent successful to {raj} members breaking')
                            break

                        if flood == 5:
                            print('flood errors breaking')
                            print('total sent user ===', added)
                            break

                        if peer == 5:
                            print('peer flood errors breaking')
                            print('total sent user ===', added)
                            break

                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total sent user ===', added)
                            break
                        
                        namess = names.get_first_name()
                        numb = str(row['numbers'])
                        username = utils.parse_phone(numb)
                        #peers = PeerUser(username)
                        try:
                            added_member += 1
                            await client.import_contacts([InputPhoneContact(username, namess)])
                            print("Contact Added ", username)
                            stop = stop + 1
                            added = added + 1
                            time.sleep(HackingZone_dev)
                            
                        except UserPrivacyRestricted:
                            await asyncio.sleep(random.randint(2,3))
                            
                            
                        except UserChannelsTooMuch:
                            await asyncio.sleep(0)
                            
                        except PeerFlood as e:
                            print('PeerFloodError', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            peer = peer + 1

                        except UserBannedInChannel as e:
                            print('User Banned In Channel Error', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            userbanned = userbanned + 1

                        except FloodWait as e:
                            print('FloodWait', nu)
                            await asyncio.sleep(random.randint(2,5))
                            nu = nu + 1
                            flood = flood + 1

                        except RPCError as e:
                             status = e.__class__.__name__
                             print(f'{status}')





                        except:
                            traceback.print_exc()
                            print(f"Unexpected Error")

            a += 1

    asyncio.run(mainn())              
    
    
def addtocontactbygroup():

    config = configparser.ConfigParser()
    config.read("config.ini")
    stacno = config['HackingZone']['StartingAccount']
    endacno = config['HackingZone']['EndAccount']
    api_hash = config["HackingZone"]['api_hash']
    api_id = config["HackingZone"]['api_id']
    
    groupshub = str(input("Give Group Username or Private Link: "))
    raj = int(input("How many Members you want to add per account: "))
    
    print(Style.BRIGHT + Fore.GREEN + 'Enter Delay Time Per Request 0 For None : ')
    HackingZone_dev = int(input())
    
    phone = []

    with open('phone.csv', 'r') as delta_obj:
        csv_reader = csv.reader(delta_obj)
        list_of_phone = tuple(csv_reader)
        for phone_ in list_of_phone:
            phone.append(int(phone_[0]))
        pphone = phone

    print(f'Total account: {str(len(phone))}')

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

            async with Client(f'sessions/{phone}', api_id, api_hash) as client:

                try:
                     await client.join_chat(groupshub)
                except UserAlreadyParticipant:
                     pass
                except Exception as e:
                     print('Failed to connect:', e)
                     return
                try:
                     my_group_entity = await client.get_chat(groupshub)
                except Exception as e:
                     print('Failed to connect:', e)
                     return
                
                nu = 1
                stop = 0
                flood = 0
                added = 0
                peer = 0
                userbanned = 0
                contacttrial = 0

                with open(f'numbers.csv', mode='r', encoding='UTF-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for i, row in enumerate(csv_reader):

                        with open('done.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for roww in reader:
                                if len(roww) > 0:
                                    added_members = int(roww[0])

                        with open("done.csv", mode='w', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow([added_member + 1])

                        if i < added_members:
                            continue

                        if stop == raj:
                            print(f'Total added {raj} members breaking')
                            break

                        if flood == 5:
                            print('flood errors breaking')
                            print('total added user ===', added)
                            break

                        if peer == 5:
                            print('peer flood errors breaking')
                            print('total added user ===', added)
                            break

                        if userbanned == 5:
                            print('UserBannedInChannelError errors breaking')
                            print('total added user ===', added)
                            break
                        
                        if contacttrial == 10:
                            print('Accounts Number Check Flood breaking')
                            print('total added user ===', added)
                            
                        numb = str(row['numbers'])
                        username = utils.parse_phone(numb)
                        print(username)
                        
                        try:
                            userinfo = await client.invoke(functions.contacts.ResolvePhone(phone=f'{username}'))
                            print(userinfo)
                            print(userinfo.users)
                            print("Number Valid")
                            for user in userinfo.users:
                                print(user.id)
                                user_id = user.id
                                first_name = user.first_name
                                user_idd = await client.resolve_peer(int(user_id))
                                access_hash = user_idd.access_hash
                                try:
                                    added_member += 1
                                    await client.add_chat_members(my_group_entity.id, user_idd.user_id, access_hash)
                                    print("Member Added - ", first_name)
                                    stop = stop + 1
                                    added = added + 1
                                    time.sleep(HackingZone_dev)
                            
                                except UserPrivacyRestricted:
                                    await asyncio.sleep(random.randint(2,3))
                            
                            
                                except UserChannelsTooMuch:
                                    await asyncio.sleep(0)
                            
                                except PeerFlood as e:
                                    print('PeerFloodError', nu)
                                    await asyncio.sleep(random.randint(2,5))
                                    nu = nu + 1
                                    peer = peer + 1

                                except UserBannedInChannel as e:
                                    print('User Banned In Channel Error', nu)
                                    await asyncio.sleep(random.randint(2,5))
                                    nu = nu + 1
                                    userbanned = userbanned + 1

                                except FloodWait as e:
                                    print('FloodWait', nu)
                                    await asyncio.sleep(random.randint(2,5))
                                    nu = nu + 1
                                    flood = flood + 1

                                except RPCError as e:
                                    status = e.__class__.__name__
                                    print(f'{status}')

                                except:
                                    traceback.print_exc()
                                    print(f"Unexpected Error")
                                
                        except Exception as e:
                            print(e)
                            nu = nu + 1
                            contacttrial = contacttrial + 1
            a += 1

    asyncio.run(mainn())              
