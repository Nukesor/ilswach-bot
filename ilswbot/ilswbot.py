"""Ilsw bot."""
import traceback
import urllib.error
import urllib.request
from ilswbot.db import get_session
from ilswbot.subscriber import Subscriber
from ilswbot.config import (
    API_URL,
    TELEGRAM_API_KEY,
    PERMANENT_SUBS_ENABLED,
    ONE_TIME_SUB_ENABLED,
)

from telegram.ext import (
    CommandHandler,
    Filters,
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
        self.sleeping = None
        self.subscribers = []
        self.updater = Updater(token=TELEGRAM_API_KEY)

        # Add reoccurring jobs
        job_queue = self.updater.job_queue
        job_queue.run_repeating(self.answer_subscribers, interval=10, first=0)

        # Create handler
        message_handler = MessageHandler(Filters.text, self.process)
        stop_handler = CommandHandler('stop', self.stop)
        start_handler = CommandHandler('start', self.start)
        subscribe_handler = CommandHandler('subscribe', self.subscribe)
        unsubscribe_handler = CommandHandler('unsubscribe', self.unsubscribe)

        # Add handler
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(message_handler)
        dispatcher.add_handler(stop_handler)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(subscribe_handler)
        dispatcher.add_handler(unsubscribe_handler)

        # Start to poll messages
        self.updater.start_polling()

    def main(self):
        """Run the main loop of the bot."""
        self.updater.idle()

    def start(self, bot, update):
        """Start the bot."""
        try:
            session = get_session()
            chat_id = update.message.chat_id
            subscriber = Subscriber.get_or_create(session, chat_id)
            subscriber.active = True

            session.add(subscriber)
            session.commit()

            text = "I'm spying on Lukas :3"
            bot.sendMessage(chat_id=chat_id, text=text)
        except Exception as e:
            print('Error in function `start`.')
            print(traceback.format_exc())
            pass
        finally:
            session.remove()

    def subscribe(self, bot, update):
        """Start the bot."""
        try:
            session = get_session()
            chat_id = update.message.chat_id
            subscriber = Subscriber.get_or_create(session, chat_id)
            subscriber.subscribed = True

            session.add(subscriber)
            session.commit()

            text = "You're now subscribed."
            bot.sendMessage(chat_id=chat_id, text=text)
        except Exception as e:
            print('Error in function `subscribe`.')
            print(traceback.format_exc())
            pass
        finally:
            session.remove()

    def unsubscribe(self, bot, update):
        """Start the bot."""
        try:
            session = get_session()
            chat_id = update.message.chat_id
            subscriber = Subscriber.get_or_create(session, chat_id)
            subscriber.subscribed = False

            session.add(subscriber)
            session.commit()

            text = "You're now unsubscribed."
            bot.sendMessage(chat_id=chat_id, text=text)
        except Exception as e:
            print('Error in function `subscribe`.')
            print(traceback.format_exc())
            pass
        finally:
            session.remove()

    def stop(self, bot, update):
        """Stop the bot."""
        try:
            session = get_session()
            chat_id = update.message.chat_id
            subscriber = Subscriber.get_or_create(session, chat_id)
            subscriber.active = False
            session.add(subscriber)
            session.commit()

            text = "Stopped spying on Lukas :("
            bot.sendMessage(chat_id=chat_id, text=text)
        except Exception as e:
            print('Error in function `stop`.')
            print(traceback.format_exc())
            pass
        finally:
            session.remove()

    def process(self, bot, update):
        """Check if anybody asked for lukas's status and anser them."""
        try:
            session = get_session()
            message = update.message.text.lower()
            chat_id = update.message.chat_id
            subscriber = Subscriber.get_or_create(session, chat_id)
            if subscriber.active is False:
                return

            # Flame Lukas, if he asks for his own sleep status. Subscribing is allowed
            if 'lukasovich' == update.message.from_user.username.lower():
                if 'wach' in message:
                    bot.sendMessage(
                        chat_id=update.message.chat_id,
                        text='Halt die Fresse Lukas >:S',
                    )
                    return

            # Lukas mentioned and wach in one sentence.
            lukas_names = ['lukas', 'lulu']
            if len(list(filter(lambda name: name in message, lukas_names))) > 0 and 'wach' in message:

                success, response = self.get_lukas_status()
                if success and response == 'NEIN' and not subscribe.one_time_sub:
                    subscriber.one_time_sub = True
                    session.add(subscriber)
                bot.sendMessage(chat_id=chat_id, text=response)

            session.commit()

        except Exception as e:
            print('Error in function `process`.')
            print(traceback.format_exc())
            pass
        finally:
            session.remove()

    def get_lukas_status(self):
        """Poll the ilsw api for lukas's sleep status."""
        try:
            status = urllib.request.urlopen(API_URL).read()
            return True, status.decode('utf-8')
        except urllib.error.HTTPError:
            return False, 'Jo. Die Api ist im Sack.'

    def answer_subscribers(self, bot, job):
        """Check if Lukas is now awake and notify everybody who asked, while he was sleeping."""
        try:
            session = get_session()
            success, api_response = self.get_lukas_status()

            if not ONE_TIME_SUB_ENABLED:
                # Answer one time subscriptions
                subscribers = session.query(Subscriber) \
                    .filter(Subscriber.one_time_sub == True) \
                    .filter(Subscriber.subscribed == False) \
                    .all()
                if len(subscribers) > 0:
                    if success and 'JA' not in api_response:
                        return
                    for subscriber in subscribers:
                        response = "Leute, Lukas is grad aufgewacht!"
                        subscriber.one_time_sub = False
                        session.add(subscriber)
                        bot.sendMessage(chat_id=subscriber.chat_id, text=response)
                session.commit()

            # Answer permanent subscriptions
            if not PERMANENT_SUBS_ENABLED:
                subscribers= session.query(Subscriber) \
                    .filter(Subscriber.subscribed == True) \
                    .all()
                if len(self.subscribers) > 0 and self.status_changed(start_polling):
                    for subscriber in subscribers:
                        if self.sleeping:
                            response = "Leute, Lukas is eingeschlafen!"
                        else:
                            response = "Leute, Lukas is grad aufgewacht!"
                        bot.sendMessage(chat_id=subscriber.chat_id, text=response)


        except Exception as e:
            print('Error in function `answer_subscribers`.')
            print(traceback.format_exc())
            pass
        finally:
            session.remove()

    def status_changed(self, status):
        status = True if status == 'JA' else False
        if self.sleeping is None:
            self.sleeping = status
            return False

        if self.sleeping == status:
            return False
        else:
            self.sleeping = status
            return True
