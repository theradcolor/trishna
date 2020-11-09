#!/usr/bin/env python3

import os
from requests import post

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram sendMessage func()
def send_Message(MESSAGE, CHAT):

    # Declare the ID of GROUP/CHANNEL
    if CHAT == "CHNL":
        CHAT_ID = os.getenv("CHANNEL_ID")
    elif CHAT == "GRP":
        CHAT_ID = os.getenv("CHAT_ID")
    elif CHAT == "PVT_GRP":
        CHAT_ID = os.getenv("PVT_CHAT_ID")
    else:
        print("CHAT_ID not declared!")

    # TG web API URL
    TG_API_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/SendMessage'
    DATA = {
        'chat_id': CHAT_ID,
        'text': MESSAGE,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': 'true'
    }
    
    post(TG_API_URL, data=DATA)