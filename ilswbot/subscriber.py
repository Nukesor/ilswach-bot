"""The sqlite model for a subscriber."""
from ilswbot.db import base

from sqlalchemy import Column, String, Boolean


class Subscriber(base):
    """The sqlite model for a subscriber."""

    __tablename__ = 'subscriber'

    chat_id = Column(String(100), primary_key=True)
    active = Column(Boolean(), nullable=False, default=False)
    waiting = Column(Boolean(), nullable=False, default=False)

    def __init__(self, chat_id):
        """Create a new subscriber."""
        self.chat_id = chat_id

    @staticmethod
    def get_or_create(session, chat_id):
        """Get or create a new subscriber."""
        subscriber = session.query(Subscriber).get(chat_id)
        if not subscriber:
            subscriber = Subscriber(chat_id)
            session.add(subscriber)
            session.commit()
            subscriber = session.query(Subscriber).get(chat_id)

        return subscriber
