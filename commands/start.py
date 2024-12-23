from telegram import Update, ForceReply
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a start message to the user."""
    user = update.effective_user
    await update.message.reply_html(
        rf" Hii {user.mention_html()} Welcome to the Persist Ventures Bot! Use /help to see available commands.",
        reply_markup=ForceReply(selective=True),
    )
