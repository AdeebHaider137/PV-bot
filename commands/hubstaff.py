import json
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

# In-memory storage for demonstration purposes (replace with a database for production)
user_tokens = {}

async def hubstaff(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the process to link the user's Hubstaff account."""
    await update.message.reply_text(
        "Please provide your Hubstaff API token to link your account. You can find it in your Hubstaff account settings."
    )
    # Set a context flag to expect the user's API token
    context.user_data['awaiting_hubstaff_token'] = True

async def save_hubstaff_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Validate and save the Hubstaff API token provided by the user."""
    if context.user_data.get('awaiting_hubstaff_token', False):
        # Get the token from the user's message
        token = update.message.text.strip()

        # Attempt to validate the token with the Hubstaff API
        headers = {"Authorization": f"Bearer {token}"}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get("https://api.hubstaff.com/v2/users/me", headers=headers) as response:
                    if response.status == 200:
                        # Token is valid
                        user_data = await response.json()
                        user_id = update.effective_user.id
                        user_tokens[user_id] = token  # Save token (replace with secure storage in production)
                        context.user_data['awaiting_hubstaff_token'] = False
                        await update.message.reply_text(
                            f"Your Hubstaff account has been linked successfully! Welcome, {user_data['name']}."
                        )
                    else:
                        # Handle invalid token
                        error_message = await response.text()
                        await update.message.reply_text(
                            f"Failed to link your Hubstaff account. Please check your token and try again. ({response.status})"
                        )
            except aiohttp.ClientError as e:
                # Handle connection errors
                await update.message.reply_text(
                    "There was an error connecting to the Hubstaff API. Please try again later."
                )
    else:
        await update.message.reply_text(
            "Please use /hubstaff to start linking your account first."
        )

# Handlers
hubstaff_handler = CommandHandler("hubstaff", hubstaff)
save_token_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, save_hubstaff_token)

