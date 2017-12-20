"""Helper class to get a database engine and to get a session."""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ilswbot.config import SQL_URI

engine = create_engine(SQL_URI, poolclass=NullPool)
base = declarative_base(bind=engine)


@contextmanager
def session_scope():
    """Get a new scoped session."""
    session = scoped_session(sessionmaker(bind=engine))
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        session.remove()
        raise
    finally:
        session.remove()
