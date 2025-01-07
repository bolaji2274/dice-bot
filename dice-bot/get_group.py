from telethon import TelegramClient
import asyncio

# Replace with your Telegram API credentials
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'

# Script to Find Group by Title or Username

# The group title you want to search for
TARGET_GROUP_TITLE = "AZIOX" # Replace with your group title


# Initialize the Telegram client
client = TelegramClient('group_resolver_bot', API_ID, API_HASH)

async def find_group():
    async with client:
        print("Fetching your groups...")
        async for dialog in client.iter_dialogs():
            # Check if the dialog title matches the target group title
            if dialog.is_group and dialog.name == TARGET_GROUP_TITLE:
                print(f"Group found: {dialog.name}")
                print(f"Group ID: {dialog.id}")
                print(f"Group Username: {dialog.entity.username}")
                return dialog

        print("Group not found. Please ensure the title is correct.")

# Run the script
asyncio.run(find_group())
