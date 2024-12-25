from flask import Flask
from threading import Thread
import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler
from commands.add_task import add_task
from commands.daily_update import daily_update
from commands.feedback import feedback
from commands.help_command import help_command
from commands.leave import leave
from commands.listtask import list_task
from commands.start import start
from commands.stats import stats


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Telegram Bot is running."

def run_flask():
    web_app.run(host="0.0.0.0", port=8080)


def run_bot():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")

    application = ApplicationBuilder().token(TOKEN).build()

    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dailyupdate", daily_update))
    application.add_handler(CommandHandler("leave", leave))
    application.add_handler(CommandHandler("addtask", add_task))
    application.add_handler(CommandHandler("listtask", list_task))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("feedback", feedback))

    logging.info("Starting the Telegram bot...")
    application.run_polling()

if __name__ == "__main__":
    
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    
    run_bot()