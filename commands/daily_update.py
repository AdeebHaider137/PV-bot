from telegram import Update, ForceReply
from telegram.ext import ContextTypes, CommandHandler
import aiohttp
import os

HUBSTAFF_ACCESS_TOKEN = os.getenv("HUBSTAFF_ACCESS_TOKEN")
YOUR_PROJECT_ID = os.getenv("YOUR_PROJECT_ID")

async def daily_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prompt the user to submit their daily update."""
    await update.message.reply_text(
        "Please submit your daily update by replying to this message."
    )

async def handle_daily_update_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the user's reply and submit the daily update to Hubstaff."""
    note = update.message.text or "Daily update submitted via Telegram bot."
    headers = {
        "Authorization": f"Bearer {HUBSTAFF_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"notes": note, "project_id": YOUR_PROJECT_ID}

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.hubstaff.com/v2/activities", headers=headers, json=payload) as response:
            if response.status == 201:
                await update.message.reply_text("Daily update submitted successfully!")
            else:
                error_message = await response.text()
                await update.message.reply_text(f"Failed to submit update. Error: {error_message}")

daily_update_handler = CommandHandler("dailyupdate", daily_update)
