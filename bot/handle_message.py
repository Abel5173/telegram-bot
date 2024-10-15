import logging
import requests
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler, CallbackContext, CallbackQueryHandler
from bot.utils import send_options


ACCESS_KEY = "Qp7yCOEeuJfA_eOx0MOjDYpHyrs6MVJazOK1l4zARhQ"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    orientation = context.user_data.get('orientation', '')
    color = context.user_data.get('color', '')

    search_url = f"https://api.unsplash.com/search/photos?per_page=10&query={user_message}&client_id={ACCESS_KEY}"

    if orientation:
        search_url += f"&orientation={orientation}"
    if color:
        search_url += f"&color={color}"

    try:
        response = requests.get(search_url, timeout=5)  # Added timeout
        response.raise_for_status()  # Check if request was successful

        # Process images as before
        photo_data = response.json()

        if photo_data['results']:
            for photo in photo_data['results']:
                # Extract the necessary information
                image_url = photo['urls']['regular']
                photographer = photo['user']['name']
                likes = photo['likes']
                description = photo['alt_description'] or "No description available."

                # Prepare the message text with photo details
                message_text = (
                    f"📸 Photo by: *{photographer}*\n"
                    f"❤️ Likes: {likes}\n"
                    f"📝 Description: {description}\n"
                    f"[View on Unsplash]({photo['links']['html']})"  
                )

                # Send the image with the details
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=message_text, parse_mode='Markdown')

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No images found")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching images: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error fetching images. Please try again later.")

    await send_options(update, context)
