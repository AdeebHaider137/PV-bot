import json
import os
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

# Temporary in-memory storage for demonstration
user_hubstaff_emails = {}  # {telegram_user_id: hubstaff_email}
HUBSTAFF_ACCESS_TOKEN = os.getenv("HUBSTAFF_ACCESS_TOKEN")
headers = {"Authorization": f"Bearer {HUBSTAFF_ACCESS_TOKEN}"}

async def hubstaff(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prompt the user to link their Hubstaff account."""
    await update.message.reply_text(
        "Please provide your Hubstaff email to link your account."
    )
    context.user_data['awaiting_hubstaff_email'] = True

async def verify_and_link_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Verify the user's email and link them to their Hubstaff account."""
    if context.user_data.get('awaiting_hubstaff_email', False):
        email = update.message.text.strip()

        async with aiohttp.ClientSession() as session:
            try:
                # Fetch the authenticated user's information
                headers = {"Authorization": f"Bearer {HUBSTAFF_ACCESS_TOKEN}"}
                async with session.get("https://api.hubstaff.com/v2/users", headers=headers) as response:
                    if response.status == 200:
                        users = await response.json()

                        # Check if the provided email exists in the user list
                        user = next((u for u in users['users'] if u['email'] == email), None)
                        if user:
                            # Save email and link the user
                            user_hubstaff_emails[update.effective_user.id] = email
                            context.user_data['awaiting_hubstaff_email'] = False
                            await update.message.reply_text("Your account has been linked successfully!")
                        else:
                            await update.message.reply_text("Email not found in Hubstaff. Please check and try again.")
                    else:
                        await update.message.reply_text("Failed to connect to Hubstaff. Please try again later.")
            except aiohttp.ClientError as e:
                await update.message.reply_text("An error occurred while connecting to Hubstaff. Please try again later.")
    else:
        await update.message.reply_text("Please use /hubstaff to link your account first.")
verify_user_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, verify_and_link_user)
