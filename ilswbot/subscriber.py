"""The sqlite model for a subscriber."""
from ilswbot.db import base

from sqlalchemy import Column, String, Integer, Boolean


class Subscriber(base):
    """The sqlite model for a subscriber."""

    __tablename__ = 'subscriber'

    chat_id = Column(String(100), primary_key=True)
    active = Column(Boolean(), nullable=False, default=False)
    waiting = Column(Boolean(), nullable=False, default=False)

    def __init__(self, chat_id):
        """Create a new subscriber."""
        self.chat_id = chat_id
