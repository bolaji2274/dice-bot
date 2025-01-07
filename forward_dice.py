from telethon import TelegramClient, events
import asyncio
from dotenv import load_dotenv
import os
from telethon.tl.types import PeerChat, PeerChannel

load_dotenv()
# Replace with your Telegram API credentials
# API_ID = 'YOUR_API_ID'
# API_HASH = 'YOUR_API_HASH'

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    raise ValueError("API credentials are missing. Please set TELEGRAM_API_ID and TELEGRAM_API_HASH.")

# Initialize Telegram client
client = TelegramClient('my_session', int(API_ID), API_HASH)


# Replace with the group ID or username
# TARGET_GROUP = 'your_target_group_id_or_username'
TARGET_GROUP = -4671858349

# Initialize the Telegram client
client = TelegramClient('dice_forward_bot', API_ID, API_HASH)

async def forward_dice():
    async with client:
        print("Bot is running...")
        
        # Fetch recent messages from Saved Messages
        async for message in client.iter_messages('me', limit=5):
            print(f"Message: {message.message}")
            if message.dice:  # Check if the message is a dice
                print(f"Dice result found: {message.dice.value}")

                # Send a new dice message to the target group
                await client.send_message(TARGET_GROUP, file=message.media)
                
                # Copy the message to the target group (removes forward mark)
                new_message = f"🎲 Dice result: {message.dice.value}"
                await client.send_message(TARGET_GROUP, new_message)

                print(f"Dice sent to group with result: {message.dice.value}")
                print(f"Dice result copied to group: {new_message}")
                
                
                 # Send a new dice to the target group (result will be random)
                # dice_message = await client.send_dice(TARGET_GROUP, emoji="🎲")

                # # Follow up with the correct result in a separate message
                # result_message = f"Original Dice Result: 🎲 {message.dice.value}"
                # await client.send_message(TARGET_GROUP, result_message)
                
                # print(f"Dice and result sent to group: {TARGET_GROUP}")
                
                return  # Exit after forwarding one dice
        # try:
        #     dice_message = await client.send_message(TARGET_GROUP, file='🎲')
        #     print(f"Dice message sent with value: {dice_message.dice.value}")
        # except Exception as e:
        #     print(f"Error sending dice message: {e}")

        print("No dice message found in Saved Messages.")

# Run the script
asyncio.run(forward_dice())

# async def find_group():
#     async with client:
#         print("Fetching your groups...")
#         async for dialog in client.iter_dialogs():
#             # Check if the dialog title matches the target group title
#             if dialog.is_group and dialog.name == TARGET_GROUP:
#                 print(f"Group found: {dialog.name}")
#                 print(f"Group ID: {dialog.id}")
#                 # print(f"Group Username: {dialog.entity.username}")
#                 return dialog

#         print("Group not found. Please ensure the title is correct.")

# # Run the script
# asyncio.run(find_group())
