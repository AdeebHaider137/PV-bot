from telegram import Update, ForceReply
from telegram.ext import ContextTypes

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "We value your feedback! Please reply to this message or send a mail to kaxmiadeeb@gmail.com with your feedback."
    )