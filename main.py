import logging
import os
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes)

# Import command modules
from commands.add_task import add_task
from commands.daily_update import daily_update
from commands.feedback import feedback
from commands.help_command import help_command
from commands.leave import leave
from commands.listtask import list_task
from commands.start import start
from commands.stats import stats

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a message to the user."""
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and update.effective_user:
        await update.effective_message.reply_text(
            "An unexpected error occurred. Please try again later."
        )

if __name__ == "__main__":
    # Load the bot token from environment variable
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")

    # Initialize the bot application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dailyupdate", daily_update))
    application.add_handler(CommandHandler("leave", leave))
    application.add_handler(CommandHandler("addtask", add_task))
    application.add_handler(CommandHandler("listtask", list_task))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("feedback", feedback))

    # Add error handler
    application.add_error_handler(error_handler)

    # Run the bot
    logging.info("Starting the bot...")
    application.run_polling()
