"""A bot which checks if Lukas is already awake.

If Lukas isn't awake, we notify everybody who asked,
as soon as he wakes up!. Critical importance!!!
"""

from ilswbot.session import session_wrapper, job_session_wrapper
from ilswbot.subscriber import Subscriber
from ilswbot.config import config
from ilswbot.lukas_helper import get_lukas_status, status_changed

from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


# The current state of lukas
sleeping = None


@session_wrapper()
def start(bot, update, session):
    """Start the bot."""
    chat_id = update.message.chat_id
    subscriber = Subscriber.get_or_create(session, chat_id)
    subscriber.active = True

    session.add(subscriber)
    session.commit()

    text = "I'm spying on Lukas :3"
    bot.sendMessage(chat_id=chat_id, text=text)


@session_wrapper()
def subscribe(bot, update, session):
    """Start the bot."""
    chat_id = update.message.chat_id
    subscriber = Subscriber.get_or_create(session, chat_id)
    subscriber.subscribed = True

    session.add(subscriber)
    session.commit()

    text = "You're now subscribed."
    bot.sendMessage(chat_id=chat_id, text=text)


@session_wrapper()
def unsubscribe(bot, update, session):
    """Start the bot."""
    chat_id = update.message.chat_id
    subscriber = Subscriber.get_or_create(session, chat_id)
    subscriber.subscribed = False

    session.add(subscriber)
    session.commit()

    text = "You're now unsubscribed."
    bot.sendMessage(chat_id=chat_id, text=text)


@session_wrapper()
def stop(bot, update, session):
    """Stop the bot."""
    chat_id = update.message.chat_id
    subscriber = Subscriber.get_or_create(session, chat_id)
    subscriber.active = False
    session.add(subscriber)
    session.commit()

    text = "Stopped spying on Lukas :("
    bot.sendMessage(chat_id=chat_id, text=text)


@session_wrapper()
def process(bot, update, session):
    """Check if anybody asked for lukas's status and anser them."""
    message = update.message.text.lower()
    chat_id = update.message.chat_id
    subscriber = Subscriber.get_or_create(session, chat_id)
    if subscriber.active is False:
        return

    # Flame Lukas, if he asks for his own sleep status. Subscribing is allowed
    from_user = update.message.from_user.username.lower()
    if from_user.username is not None and 'lukasovich' == from_user.username.lower():
        if 'wach' in message:
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text='Halt die Fresse Lukas >:S',
            )
            return

    # Lukas mentioned and wach in one sentence.
    lukas_names = ['lukas', 'lulu']
    if len(list(filter(lambda name: name in message, lukas_names))) > 0 and 'wach' in message:

        success, response = get_lukas_status()
        if success and response.lower() == 'nein' and not subscriber.one_time_sub:
            subscriber.one_time_sub = True
            session.add(subscriber)
        bot.sendMessage(chat_id=chat_id, text=response)

    session.commit()


@job_session_wrapper()
def answer_subscribers(context, session):
    """Check if Lukas is now awake and notify everybody who asked, while he was sleeping."""
    success, api_response = get_lukas_status()
    if not success:
        return

    if config['settings']['one_time_subs']:
        # Answer one time subscriptions
        subscribers = session.query(Subscriber) \
            .filter(Subscriber.one_time_sub.is_(True)) \
            .filter(Subscriber.subscribed.is_(False)) \
            .all()
        if len(subscribers) > 0:
            if 'ja' not in api_response.lower():
                return
            for subscriber in subscribers:
                response = "Leute, Lukas is grad aufgewacht!"
                subscriber.one_time_sub = False
                session.add(subscriber)
                context.bot.sendMessage(chat_id=subscriber.chat_id, text=response)
        session.commit()

    # Answer permanent subscriptions
    if config['settings']['permanent_subs']:
        subscribers = session.query(Subscriber) \
            .filter(Subscriber.subscribed.is_(True)) \
            .all()
        global sleeping
        if len(subscribers) > 0 and status_changed(api_response):
            for subscriber in subscribers:
                if sleeping:
                    response = "Leute, Lukas is eingeschlafen!"
                else:
                    response = "Leute, Lukas is grad aufgewacht!"
                context.bot.sendMessage(chat_id=subscriber.chat_id, text=response)


def start_the_christmas_spirit(update, context):
    """Respond to startTheChristmasSpirit."""
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=open('./pics/christmas_life.jpg', 'rb'))


def thug_life(update, context):
    """Respond to thug life."""
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=open('./pics/thug_life.jpg', 'rb'))


def goodbot(update, context):
    """Respond to goodbot."""
    chat_id = update.message.chat_id
    context.bot.sendMessage(chat_id=chat_id, text=":3")


# Initialize telegram bot and all needed variables.
updater = Updater(
    token=config['telegram']['api_key'],
    use_context=True,
)

# Add reoccurring jobs
job_queue = updater.job_queue
job_queue.run_repeating(answer_subscribers, interval=10, first=0)

# Create handler
message_handler = MessageHandler(Filters.text, process)
stop_handler = CommandHandler('stop', stop)
start_handler = CommandHandler('start', start)
start_spirit_handler = CommandHandler('start_the_christmas_spirit', start_the_christmas_spirit)
goodbot_handler = CommandHandler('goodbot', goodbot)
thuglife_handler = CommandHandler('thuglife', thug_life)

# Add handler
dispatcher = updater.dispatcher
dispatcher.add_handler(message_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(start_spirit_handler)
dispatcher.add_handler(goodbot_handler)
dispatcher.add_handler(thuglife_handler)

if config['settings']['permanent_subs']:
    subscribe_handler = CommandHandler('subscribe', subscribe)
    unsubscribe_handler = CommandHandler('unsubscribe', unsubscribe)
    dispatcher.add_handler(subscribe_handler)
    dispatcher.add_handler(unsubscribe_handler)
