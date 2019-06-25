#!/bin/env python
"""Drop and create a new database with schema."""

from sqlalchemy_utils.functions import database_exists, create_database
from ilswbot.db import engine, base
from ilswbot.subscriber import Subscriber # noqa


db_url = engine.url
if not database_exists(db_url):
    create_database(db_url)
    base.metadata.create_all()
