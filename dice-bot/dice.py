import sys
import pygame
import random
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os
import time
from PIL import Image

load_dotenv()

# Telegram API credentials
API_ID = os.getenv("TELEGRAM_API_ID") # Replace with your API ID and Hash
API_HASH = os.getenv("TELEGRAM_API_HASH") # Replace with your API ID and Hash
PHONE_NUMBER = 'your_telegram_number'  # +94 Replace with your phone number
SESSION_NAME = "dice_bot"

group = 'your_group_id' # Replace with your group ID or username (e.g., 'tgbots') 

# Function to retrieve the dice result from Telegram
def get_dice_result(client):
    try:
        messages = client.get_messages('me', limit=10)
        print("Messages fetched successfully.")
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return None

    for msg in messages:
        if msg.dice:
            return msg.dice.value
    return None

# Function to draw the dice face in Pygame (with animated rolling effect)
def draw_dice_face(screen, result, size=100, background_color=(0, 0, 0)):
    dice_color = (230, 230, 230)
    border_color = (0, 0, 0)  # Black border for the dice
    dot_color = (255, 0, 0) if result == 1 else (0, 0, 0)  # Red for result 1, Black otherwise
    border_width = 10  # Border thickness
    radius = 20  # Rounded corners for the dice

    # Fill the screen with the background color (dark)
    screen.fill(background_color)

    # Dice border (rounded corners)
    pygame.draw.rect(screen, dice_color, (75, 75, size, size), border_radius=radius)

    # Positions for dots based on the dice number
    positions = {
        1: [(150, 150)],  # Center
        2: [(115, 115), (185, 185)],  # Top-left, bottom-right
        3: [(115, 115), (150, 150), (185, 185)],  # Top-left, center, bottom-right
        4: [(115, 115), (115, 185), (185, 115), (185, 185)],  # Four corners
        5: [(115, 115), (115, 185), (150, 150), (185, 115), (185, 185)],  # Four corners and center
        6: [(115, 115), (115, 150), (115, 185), (185, 115), (185, 150), (185, 185)]  # Two columns of three dots
    }

    # Draw the dots for the specified result
    for pos in positions[result]:
        pygame.draw.circle(screen, dot_color, pos, 10)  # 15px radius for each dot

# Function to simulate a smooth rolling dice animation
def roll_dice_animation(client, result, output_file='dice_result.png'):
    pygame.init()

    # Set up screen for animation
    screen = pygame.Surface((300, 300), pygame.SRCALPHA)  # Use SRCALPHA for transparency
    size = 150
    frames = 30  # Number of frames for the roll animation
    roll_results = [random.choice([1, 2, 3, 4, 5, 6]) for _ in range(frames)]

    # Loop through the frames to create the rolling effect (in memory)
    for i in range(frames):
        screen.fill((0, 0, 0, 0))  # Transparent background for animation
        draw_dice_face(screen, roll_results[i], size, background_color=(0, 0, 0))

    # Finally, draw the final result after the roll
    screen.fill((0, 0, 0, 0))  # Transparent background for the final frame
    draw_dice_face(screen, result, size, background_color=(0, 0, 0))
    pygame.image.save(screen, output_file)  # Save only the final result

    # Convert the saved image to a .webp format (necessary for Telegram stickers)
    image = Image.open(output_file)
    image = image.convert("RGBA")  # Ensure RGBA for transparency
    webp_file = output_file.replace('.png', '.webp')
    image.save(webp_file, 'WEBP')

    # Optionally remove the original PNG file
    os.remove(output_file)

    return webp_file

# Function to send the recreated dice as a sticker to Telegram group
def send_dice_to_group(client, group_name, dice_sticker_path):
    # Send the sticker to the group using the send_file method
    client.send_file(group_name, dice_sticker_path, caption="Here is the dice roll result!")
    print(f"Dice result sent to the group '{group_name}'!")

# Main function to orchestrate the process
def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    client.connect()

    if not client.is_user_authorized():
        print("Logging in...")
        client.send_code_request(PHONE_NUMBER)
        try:
            client.sign_in(PHONE_NUMBER, input("Enter the code you received: "))
        except Exception as e:
            if "SessionPasswordNeededError" in str(e):
                password = input("Enter your two-step verification password: ")
                client.sign_in(password=password)
            else:
                print(f"Unexpected error: {e}")
                sys.exit()

    # Retrieve dice result from Telegram
    dice_result = get_dice_result(client)
    if dice_result is None:
        print("No dice roll found in recent messages.")
        sys.exit()

    print(f"Extracted dice result: {dice_result}")
    dice_sticker = roll_dice_animation(client, dice_result)  # Create the animated dice roll and convert to .webp

    
    
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


    target_group = group  # Replace with your group username or ID
    send_dice_to_group(client, target_group, dice_sticker)

    client.disconnect()

if __name__ == "__main__":
    main()