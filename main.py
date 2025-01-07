from telethon import TelegramClient
import asyncio
import random
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    raise ValueError("API credentials are missing. Please set TELEGRAM_API_ID and TELEGRAM_API_HASH.")

# Initialize Telegram client
client = TelegramClient('dice_forward_bot', int(API_ID), API_HASH)

TARGET_GROUP = -4671858349  # Replace with your target group ID

async def forward_matching_dice():
    async with client:
        print("Bot is running...")
        
        # Fetch recent messages from Saved Messages
        async for message in client.iter_messages('me', limit=5):
            if message.dice:
                saved_dice_value = message.dice.value
                print(f"Captured dice result: {saved_dice_value}")
                
                # Roll multiple dice until we match the saved value
                match_found = False
                while not match_found:
                    # Roll a new dice
                    rolled_value = random.randint(1, 6)  # Simulate a dice roll
                    print(f"Rolled dice value: {rolled_value}")
                    
                    if rolled_value == saved_dice_value:
                        match_found = True
                        # Send the matching dice result to the target group
                        await client.send_message(TARGET_GROUP, f"🎲 Dice result: {rolled_value}")
                        print(f"Matching dice result sent to group: {rolled_value}")
                    else:
                        print(f"No match. Rolling again...")

                return  # Exit after finding a matching dice

        print("No dice message found in Saved Messages.")

# Run the script
asyncio.run(forward_matching_dice())
