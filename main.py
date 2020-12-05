#!/usr/bin/env python3

import os
import logging
import requests
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

MODE = os.getenv("BOT_MODE")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DRONE_TOKEN = os.getenv("DRONE_TOKEN")

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
    # See if there are 2 arguments passed
    try:
        BRANCH = context.args[1]
    except IndexError:
        update.effective_message.reply_text(
            "Please define a branch/param with format: <code>/trigger repo branch/param</code>", parse_mode="html")
        raise
    REPO = context.args[0]

    # Smoll hack for our kernel repo
    if REPO == "kernel":
        REPO = "android_kernel_xiaomi_whyred"

    
    user = update.effective_user

    if user.id == 1154905452 and REPO != "fakerad":
        # Trigger for other builds using drone.io API
        logger.info("New CI build has been triggered by {} ".format(update.effective_user["id"]))
        drone_header = {"Authorization": "Bearer " + DRONE_TOKEN}

        URL='https://cloud.drone.io/api/repos/theradcolor/' + REPO + '/builds?branch=' + BRANCH
        json_out = requests.post(URL, headers=drone_header)

        update.effective_message.reply_text("<code>" + json_out.text + "</code>", parse_mode="html", disable_web_page_preview=True)

    elif REPO == "fakerad" and user.id == 1154905452 or user.id == 869226753:
        # Trigger for fakerad build of kernel
        logger.info("New fakerad build has been triggered by {} ".format(update.effective_user["id"]))

        REPO = "android_kernel_xiaomi_whyred"
        drone_header = {"Authorization": "Bearer " + DRONE_TOKEN}

        params = {'CI_KERNEL_TYPE': 'fakerad'}
        URL='https://cloud.drone.io/api/repos/theradcolor/' + REPO + '/builds?branch=' + BRANCH
        json_out = requests.post(URL, headers=drone_header, data=params)

        update.effective_message.reply_text("<code>" + json_out.text + "</code>", parse_mode="html", disable_web_page_preview=True)

    else:
        logger.info("Unauthorised access by {} ".format(update.effective_user["id"]))


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