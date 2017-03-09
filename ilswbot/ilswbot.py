#!/usr/bin/env python3

import urllib.error
import urllib.request
from ilswbot.config import TELEGRAM_API_KEY

from telegram.ext import (
    Filters,
    Job,
    MessageHandler,
    Updater,
)


class Ilsw():
    """A bot which checks if Lukas is already awake.

    If Lukas isn't awake, we notify everybody who asked,
    as soon as he wakes up!. Critical importance!!!
    """
    def __init__(self):
        """Initialize telegram bot and all needed variables."""
        self.updater = Updater(token=TELEGRAM_API_KEY)
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(MessageHandler(Filters.text, self.process))
        job_queue = self.updater.job_queue
        job_queue.put(Job(self.answer_subscribers, 10, repeat=True))
        self.updater.start_polling()

        self.last_status = None
        self.subscribers = []

    def process(self, bot, update):
        """Check if anybody asked for lukas's status and anser them."""
        names = ['lukas', 'lulu']
        message = update.message.text.lower()

        # Flame Lukas, if he asks for his own sleep status. Subscribing is allowed
        if 'lukasovich' == update.message.from_user.username.lower() \
                and 'subscribe' not in message:
            if 'wach' in message:
                bot.sendMessage(chat_id=update.message.chat_id, text='Halt die Fresse Lukas')
        elif len(list(filter(lambda name: name in message, names))) > 0 and 'wach' in message:

            # Extract message meta data
            chat_id = update.message.chat_id

            success, response = self.get_lukas_status()
            bot.sendMessage(chat_id=update.message.chat_id, text=response)
            if success and 'NEIN' in response:
                if chat_id not in self.subscribers:
                    self.subscribers.append(chat_id)

    def get_lukas_status(self):
        """Poll the ilsw api for lukas's sleep status."""
        try:
            status = urllib.request.urlopen("http://tron.je?raw=on").read()
            return True, status.decode('utf-8')
        except urllib.error.HTTPError:
            return False, 'Jo. Die Api ist im Sack.'

    def answer_subscribers(self, bot, job):
        """Check if Lukas is now awake and notify everybody who asked, while he was sleeping."""
        if len(self.subscribers) > 0:
            success, response = self.get_lukas_status()
            if success and response == 'JA':
                for subscriber in self.subscribers:
                    response = "Leute, Lukas is grad aufgewacht!"
                    bot.sendMessage(chat_id=subscriber, text=response)

                self.subscribers = []

    def main(self):
        """The main loop of the bot."""
        self.updater.idle()
