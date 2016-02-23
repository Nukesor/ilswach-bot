#!/usr/bin/env python3

import urllib.request
from telegram import Updater
from ilswbot.config import TELEGRAM_API_KEY


def process(bot, update):
    if 'lukas' in update.message.text and 'wach' in update.message.text:
        status = get_lukas_status()
        status = status.decode('utf-8')
        bot.sendMessage(chat_id=update.message.chat_id, text=status)


def get_lukas_status():
    return urllib.request.urlopen("http://ist-lukas-schon-wach.lol?raw=on").read()


def main():
    updater = Updater(token=TELEGRAM_API_KEY)
    dispatcher = updater.dispatcher
    dispatcher.addTelegramMessageHandler(process)
    updater.start_polling()
