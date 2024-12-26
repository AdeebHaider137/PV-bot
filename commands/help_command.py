from telegram import Update, ForceReply
from telegram.ext import ContextTypes

async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
    ➮ /start - Displays the start message.
    ➮ /dailyupdate - Submit your daily update.
    ➮ /hubstaff - To link Telegram with Hubstaff.
    ➮ /leave - Mark yourself as on leave.
    ➮ /help - Display this help message.
    ➮ /addtask - Add new task on hubstaff.
    ➮ /listtask - List all the hubstaff active tasks.
    ➮ /stats - Displays the hubstaff stats.
       ‣ Advanced Usage: /stats @User [today|yesterday|week|lastweek|month]
    ➮ /feedback - Used to give feedback.
    """
    await update.message.reply_text(help_text)
