import contextvars
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session_context = contextvars.ContextVar("db_session", default=None)


def transactional(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        db_session = db_session_context.get()
        if db_session:
            return func(*args, **kwargs, db_session=db_session)
        db_session = session()
        db_session_context.set(db_session)
        try:
            result = func(*args, **kwargs, db_session=db_session)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise
        finally:
            db_session.close()
            db_session_context.set(None)
        return result

    return wrap_func
