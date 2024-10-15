import logging
import requests
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler, CallbackContext, CallbackQueryHandler
from bot.handle_message import handle_message
from bot.send_random_image import send_random_image
from bot.handle_filter_selection import handle_filter_selection
from bot.utils import send_options, get_start_keyboard



# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def error_handler(update: Update, context: CallbackContext):
    logging.error(f"Update {update} caused error {context.error}")


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message and guides users to the filter options."""
    welcome_text = (
        "👋 Hello! I'm an image search bot powered by Unsplash, developed by your friendly neighborhood coder, Abel Zeleke! 🎉\n\n"
        "🚧 Just a heads up: I'm still under development! So if things go a bit cranky, just blame my coding skills, or lack of experience! 😅\n\n"
        "📸 Remember, I'm using the free version of the Unsplash API, so try not to query too many images or I might have to start a crowdfunding campaign! 💸\n\n"
        "🌐 This bot is hosted on Render, also on the free version, because, let's face it, I don't have money to pay for it... yet! 💰\n\n"
        "🛠️ I'll keep developing it until I find a job, so let's have some fun while we’re at it! Click the button below to start using filters!"
    )

    await update.message.reply_text(welcome_text, reply_markup=get_start_keyboard())


async def handle_start_selection(update: Update, context: CallbackContext):
    """Handles user selection from the /start command."""
    query = update.callback_query
    await query.answer()

    if query.data == 'set_filters':
        await filter(update, context)

    elif query.data == 'search':
        await query.edit_message_text("Please type your search term to find images!")

    elif query.data == 'random_image':
        await send_random_image(update, context)

if __name__ == '__main__':
    application = ApplicationBuilder().token('7844595585:AAG-iN-DkGzHFYa2Mf6E0_LX93sSGjvuThE').build()
    # Handle the /start command
    application.add_handler(CommandHandler("start", start))
    # Handle filter commands and selections
    application.add_handler(CommandHandler("filter", filter))
    # Separate CallbackQueryHandler for handling filter selections
    application.add_handler(CallbackQueryHandler(handle_filter_selection, pattern="^filter_"))
    # Handle any text message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Handle user selections from the start command
    application.add_handler(CallbackQueryHandler(handle_start_selection, pattern="^(set_filters|search|random_image)$"))
    application.add_error_handler(error_handler)
    application.run_polling()
