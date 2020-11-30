#!/usr/bin/env python3

import os
import logging
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

MODE = os.getenv("BOT_MODE")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if MODE == "development":
    def run(updater):
        updater.start_polling()
elif MODE == "active":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        APP_NAME = os.environ.get("APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=BOT_TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(APP_NAME, BOT_TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(update, context):
    logger.info("User {} has started the bot".format(update.effective_user["id"]))


def trigger_handler(update, context):
    update.effective_message.reply_text(
        "arg1: %s\n arg2: %s" % (context.args[0], context.args[1]))


def help_handler(update, context):
    print(context.chat_data)
    update.effective_message.reply_text(
        "<b>Personal Telegram helper BOT</b>", parse_mode="html")


# Main function!
if __name__ == '__main__':
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handlers.
    dp.add_handler(CommandHandler("start", start_handler))
    dp.add_handler(CommandHandler("trigger", trigger_handler))
    dp.add_handler(CommandHandler("help", help_handler))

    # Start Linux release watcher.
    logger.info("Starting Linux release watcher...")
    from snippets import linux_release

    # Start WireGuard release watcher.
    logger.info("Starting WireGuard release watcher...")
    from snippets import wireguard_release

    # Start updater
    logger.info("Starting bot...")
    run(updater)