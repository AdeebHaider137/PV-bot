from flask import Flask, request

app = Flask(__name__)

# Set up webhook route
@app.route(f"/{my_secret}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return "OK", 200

def main() -> None:
    """Start the bot using Webhooks."""
    logging.info("Initializing the application...")
    application = Application.builder().token(my_secret).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dailyupdate", daily_update))
    application.add_handler(CommandHandler("leave", leave))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addtask", add_task))
    application.add_handler(CommandHandler("listtask", list_task))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("feedback", feedback))

    logging.info("Setting up webhook...")
    application.bot.set_webhook(url=f"https://pv-bot-production.up.railway.app/{my_secret}")

    app.run(port=8443)
