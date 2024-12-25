import json
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

# In-memory storage for demonstration purposes (replace with a database for production)
user_tokens = {}

async def hubstaff(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prompt the user to link their Hubstaff account."""
    await update.message.reply_text(
        "To continue Please provide your Hubstaff email by replying to this message."
    )
    # Set a context flag to identify the next message as the token
    context.user_data['awaiting_token'] = True

async def save_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Save the provided Hubstaff token."""
    if context.user_data.get('awaiting_token'):
        token = update.message.text.strip()
        # Validate the token
        headers = {"Authorization": f"Bearer {token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.hubstaff.com/v2/users/me", headers=headers) as response:
                if response.status == 200:
                    # Save the token (in memory or database)
                    user_id = update.effective_user.id
                    user_tokens[user_id] = token
                    context.user_data['awaiting_token'] = False
                    await update.message.reply_text("Your Hubstaff account has been linked successfully!")
                else:
                    await update.message.reply_text("Invalid token. Please try again.")
    else:
        await update.message.reply_text("Please use /hubstaff to link your account first.")

hubstaff_handler = CommandHandler("hubstaff", hubstaff)
save_token_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, save_token)
