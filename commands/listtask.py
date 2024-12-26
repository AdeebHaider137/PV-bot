import aiohttp
import os
from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from commands.utils import load_tasks, save_tasks

HUBSTAFF_ACCESS_TOKEN = os.getenv("HUBSTAFF_ACCESS_TOKEN")
user_hubstaff_emails = {}  # {telegram_user_id: hubstaff_email}
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List tasks assigned to the user."""
    user_id = update.effective_user.id

    if user_id not in user_hubstaff_emails:
        await update.message.reply_text("You are not linked to a Hubstaff account. Use /hubstaff to link your account first.")
        return

    email = user_hubstaff_emails[user_id]

    async with aiohttp.ClientSession() as session:
        try:
            # Fetch the list of projects
            headers = {"Authorization": f"Bearer {HUBSTAFF_ACCESS_TOKEN}"}
            async with session.get("https://api.hubstaff.com/v2/projects", headers=headers) as projects_response:
                if projects_response.status == 200:
                    projects = await projects_response.json()

                    # Iterate through projects and find tasks assigned to this user
                    tasks_assigned = []
                    for project in projects['projects']:
                        project_id = project['id']
                        async with session.get(f"https://api.hubstaff.com/v2/projects/{project_id}/tasks", headers=headers) as tasks_response:
                            if tasks_response.status == 200:
                                tasks = await tasks_response.json()
                                user_tasks = [t for t in tasks['tasks'] if t['assignee']['email'] == email]
                                tasks_assigned.extend(user_tasks)

                    if tasks_assigned:
                        task_list = "\n".join([f"- {t['name']} (Project: {t['project']['name']})" for t in tasks_assigned])
                        await update.message.reply_text(f"Here are your tasks:\n{task_list}")
                    else:
                        await update.message.reply_text("You have no assigned tasks in any project.")
                else:
                    await update.message.reply_text("Failed to fetch projects. Please try again later.")
        except aiohttp.ClientError as e:
            await update.message.reply_text("An error occurred while connecting to Hubstaff. Please try again later.")
