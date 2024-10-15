import logging
import requests
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler, CallbackContext, CallbackQueryHandler


async def send_options(update: Update, context: CallbackContext):
    """Send the options keyboard without additional messages."""
    if update.message:  # Check if the update is a message
        await update.message.reply_text("Choose an option:", reply_markup=get_start_keyboard())
    elif update.callback_query:  # Check if the update is a callback query
        await update.callback_query.message.reply_text("Choose an option:", reply_markup=get_start_keyboard())


def get_filter_keyboard():
    keyboard = [
        [InlineKeyboardButton("Portrait", callback_data='filter_orientation_portrait'),
         InlineKeyboardButton("Landscape", callback_data='filter_orientation_landscape')],
        [InlineKeyboardButton("Black and White", callback_data='filter_color_black_and_white')],
        [InlineKeyboardButton("Search", callback_data='filter_search')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_start_keyboard():
    """Generates a keyboard for the /start command."""
    keyboard = [
        [InlineKeyboardButton("Set Filters", callback_data='set_filters')],
        [InlineKeyboardButton("Search", callback_data='search')],
        [InlineKeyboardButton("Random Image", callback_data='random_image')]
    ]
    return InlineKeyboardMarkup(keyboard)