"""Helper class to get a database engine and to get a session."""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ilswbot.config import SQL_URI

engine = create_engine(SQL_URI)
base = declarative_base(bind=engine)


def get_session():
    """Get a new scoped session."""
    session = scoped_session(sessionmaker(bind=engine))
    return session
