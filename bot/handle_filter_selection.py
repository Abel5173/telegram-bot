import logging
import requests
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler, CallbackContext, CallbackQueryHandler
from bot.utils import send_options, get_filter_keyboard


ACCESS_KEY = "Qp7yCOEeuJfA_eOx0MOjDYpHyrs6MVJazOK1l4zARhQ"

async def filter(update: Update, context: CallbackContext) -> None:
    """Shows filter options."""
    if update.callback_query:  # Check if the update is a callback query
        await update.callback_query.answer()  # Acknowledge the callback
        await update.callback_query.message.reply_text('Choose your filters:', reply_markup=get_filter_keyboard())


async def handle_filter_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Initialize filter_type and value
    filter_type = None
    value = None

    # Determine the filter type and value based on user selection
    if query.data.startswith("filter_orientation"):
        filter_type = 'orientation'
        value = query.data.split('_')[-1]  # Get the value (e.g., 'portrait', 'landscape')
        context.user_data['orientation'] = value
    elif query.data.startswith("filter_color"):
        filter_type = 'color'
        value = query.data.split('_')[-1]
        context.user_data['color'] = value

    # Create the search URL
    search_url = "https://api.unsplash.com/search/photos?per_page=10&query=people&client_id=" + ACCESS_KEY

    orientation = context.user_data.get('orientation', '')
    color = context.user_data.get('color', '')

    if orientation:
        search_url += f"&orientation={orientation}"
    if color:
        search_url += f"&color={color}"

    try:
        response = requests.get(search_url, timeout=15)  # Added timeout
        response.raise_for_status()  # Check if request was successful

        # Process images
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
                    f"[View on Unsplash]({photo['links']['html']})"  # Link to the Unsplash page
                )

                # Send the image with the details
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=message_text, parse_mode='Markdown')

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No images found")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching images: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error fetching images. Please try again later.")

    await send_options(update, context)

