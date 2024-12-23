from telegram import Update, ForceReply
from telegram.ext import ContextTypes
import os
async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mark yourself as on leave."""
    user = update.effective_user
    leave_message = f"{user.first_name} has marked themselves as on leave."
    await update.message.reply_text(leave_message)
    # Optionally notify admin
    admin_chat_id = os.getenv("ADMIN_CHAT_ID")
    if admin_chat_id:
        await context.bot.send_message(
            chat_id=admin_chat_id,
            text=f"Leave notification: {user.full_name} is on leave.")