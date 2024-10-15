import logging
from telegram import Update 
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler 

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the message from the user
    user_message = update.message.text

    # Send the AI's response back to the user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=user_message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    application = ApplicationBuilder().token('7844595585:AAG-iN-DkGzHFYa2Mf6E0_LX93sSGjvuThE').build()

    # Handle any text message
    application.add_handler(CommandHandler("start", start))
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    # Start the bot and handle messages
    application.run_polling()


