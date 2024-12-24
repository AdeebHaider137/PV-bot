import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
from commands.start import start
from commands.daily_update import daily_update
from commands.leave import leave
from commands.add_task import add_task
from commands.listtask import list_task
from commands.stats import stats
from commands.feedback import feedback

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
my_secret = os.getenv("BOT_TOKEN", "").strip()
if not my_secret:
    raise EnvironmentError("Environment variable BOT_TOKEN is missing or empty!")

app = Flask(__name__)

# Initialize the Telegram bot application
logging.info("Initializing the application...")
application = Application.builder().token(my_secret).build()

# Telegram command handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("dailyupdate", daily_update))
application.add_handler(CommandHandler("leave", leave))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("addtask", add_task))
application.add_handler(CommandHandler("listtask", list_task))
application.add_handler(CommandHandler("stats", stats))
application.add_handler(CommandHandler("feedback", feedback))

# Set up webhook route
@app.route(f"/{my_secret}", methods=["POST"])
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)  # Use await for async processing
        return "OK", 200
    except Exception as e:
        logging.error(f"Error processing update: {e}")
        return "Internal Server Error", 500

def main() -> None:
    """Starting the bot using Webhooks."""
    logging.info("Setting up webhook...")
    application.bot.set_webhook(url=f"https://pv-bot-production.up.railway.app/{my_secret}")

    # Run Flask app
    port = int(os.getenv("PORT", 8443))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    logging.info("Starting bot...")
    main()
