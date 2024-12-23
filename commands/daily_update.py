from telegram import Update, ForceReply
from telegram.ext import ContextTypes
async def daily_update(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prompt the user to submit their daily update."""
    await update.message.reply_text(
        "Please submit your daily update by replying to this message.")