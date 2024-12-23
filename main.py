#!/usr/bin/env python
# pyright: reportUnusedVariable=false, reportGeneralTypeIssues=false

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler

from commands.start import start
from commands.help import help_command
from commands.daily_update import daily_update
from commands.leave import leave
from commands.add_task import add_task
from commands.listtask import list_task
from commands.stats import stats
from commands.feedback import feedback

# Debugging environment variables
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
logger = logging.getLogger(__name__)

logging.info("Loading environment variables...")
my_secret = os.getenv('BOT_TOKEN', '').strip()
if not my_secret:
    raise EnvironmentError("Environment variable BOT_TOKEN is missing or empty!")

def main() -> None:
    """Start the bot."""
    logging.info("Initializing the application...")
    application = Application.builder().token(my_secret).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dailyupdate", daily_update))
    application.add_handler(CommandHandler("leave", leave))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addtask", add_task))
    application.add_handler(CommandHandler("listtask", list_task))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("feedback", feedback))

    logging.info("Running polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    logging.info("Starting bot...")
    main()
