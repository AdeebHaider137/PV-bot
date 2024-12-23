from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from datetime import datetime
from commands.utils import load_tasks, save_tasks

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    parts = message.split(", ", 2)
    if len(parts) != 3:
        await update.message.reply_text(
            "valid format. Use: Task Title: <title>, Description: <description>, Deadline: <date>"
        )
        return

    task = {
        "title": parts[0].split(": ")[1],
        "description": parts[1].split(": ")[1],
        "deadline": parts[2].split(": ")[1],
        "completed": False,
        "added_on": datetime.now().isoformat()
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    await update.message.reply_text(f"Task added: {task['title']}")