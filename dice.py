import sys
import pygame
import random
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Telegram API credentials
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE_NUMBER = '+2349155113797'  # Replace with your phone number
SESSION_NAME = "dice_forward_bot"

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
def draw_dice_face(screen, result, size=150):
    dice_color = (230, 230, 230)
    border_color = (0, 0, 0)  # Black border for the dice
    dot_color = (0, 0, 0)  # Dot color (dark grey)
    border_width = 10  # Border thickness
    radius = 20  # Rounded corners for the dice

    # Dice border (rounded corners)
    pygame.draw.rect(screen, dice_color, (75, 75, size, size), border_width, border_radius=radius)

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
        pygame.draw.circle(screen, dot_color, pos, 15)  # 15px radius for each dot

# Function to simulate a smooth rolling dice animation
def roll_dice_animation(client, result, output_file='dice_result.png'):
    pygame.init()

    # Set up screen for animation
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Rolling Dice')

    # Dice size and frame rate
    size = 150
    frames = 30  # Number of frames for the roll animation
    roll_results = [random.choice([1, 2, 3, 4, 5, 6]) for _ in range(frames)]

    # Loop through the frames to create the rolling effect
    for i in range(frames):
        screen.fill((255, 255, 255))  # Clear the screen
        draw_dice_face(screen, roll_results[i], size)
        pygame.display.update()  # Update the display to show the current frame
        time.sleep(0.05)  # Small delay for smooth transition

    # Finally, draw the final result after the roll
    screen.fill((255, 255, 255))  # Clear the screen
    draw_dice_face(screen, result, size)
    pygame.display.update()  # Show the final result

    # Save the final result as an image
    pygame.image.save(screen, output_file)
    pygame.quit()

# Function to send the recreated dice to Telegram group
def send_dice_to_group(client, group_name, dice_image='dice_result.png'):
    client.send_file(group_name, dice_image)
    print(f"Dice result sent to group '{group_name}'!")

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
    roll_dice_animation(client, dice_result)  # Create the animated dice roll

    target_group = -4671858349  # Replace with your group username or ID
    send_dice_to_group(client, target_group)

    client.disconnect()

if __name__ == "__main__":
    main()
