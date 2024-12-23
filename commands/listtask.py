from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from commands.utils import load_tasks, save_tasks

async def list_task(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text("No tasks available.")
        return

    task_list = "\n".join([
        f"{i + 1}. {task['title']} - {task['description']} (Deadline: {task['deadline']})"
        for i, task in enumerate(tasks) if not task["completed"]
    ])
    await update.message.reply_text("Active Tasks:\n" + task_list)