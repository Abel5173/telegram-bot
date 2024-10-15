import logging
import requests
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler, CallbackContext, CallbackQueryHandler
from bot.utils import send_options


ACCESS_KEY = "Qp7yCOEeuJfA_eOx0MOjDYpHyrs6MVJazOK1l4zARhQ"

async def send_random_image(update: Update, context: CallbackContext):
    """Fetch and send a random image from Unsplash with additional details."""
    random_url = "https://api.unsplash.com/photos/random?client_id=" + ACCESS_KEY
    try:
        response = requests.get(random_url, timeout=5)
        response.raise_for_status()
        photo_data = response.json()

        # Extract the necessary information
        image_url = photo_data['urls']['regular']
        photographer = photo_data['user']['name']
        likes = photo_data['likes']
        description = photo_data['alt_description'] or "No description available."

        # Prepare the message text with photo details
        message_text = (
            f"📸 Photo by: *{photographer}*\n"
            f"❤️ Likes: {likes}\n"
            f"📝 Description: {description}\n"
            f"[View on Unsplash]({photo_data['links']['html']})"  # Link to the Unsplash page
        )

        # Send the random image with the details
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=message_text, parse_mode='Markdown')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching random image: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error fetching random image. Please try again later.")

    await send_options(update, context)

