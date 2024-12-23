from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from commands.utils import load_tasks, save_tasks

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tasks = load_tasks()
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task["completed"]])
    pending_tasks = total_tasks - completed_tasks

    stats_message = (f"Task Statistics:\n"
                     f"- Total Tasks: {total_tasks}\n"
                     f"- Completed Tasks: {completed_tasks}\n"
                     f"- Pending Tasks: {pending_tasks}")
    await update.message.reply_text(stats_message)