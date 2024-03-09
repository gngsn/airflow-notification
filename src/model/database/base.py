__all__ = ['init_db', 'BaseModel', 'transactional']

import logging
from functools import wraps

from peewee import Model, PeeweeException, PostgresqlDatabase, Proxy

_database = Proxy()


def init_db(url="postgresql://postgres:postgres@localhost/postgres"):
    """ Lazy Initialize Database Connection """
    _database.initialize(PostgresqlDatabase(url))


class BaseModel(Model):
    class Meta:
        database = _database


def transactional(func):
    """ transactional decorator.
        use transaction by annotating @transactional decorator to method
    """

    @wraps(func)
    def wrap_func(*args, **kwargs):

        with _database.atomic() as transaction:
            try:
                return func(*args, **kwargs)
            except PeeweeException as pe:
                logging.error(pe)
                transaction.rollback()

    return wrap_func


def tx_db(func):
    """ transactional decorator.
        use transaction by annotating @transactional decorator to method
    """

    @wraps(func)
    def wrap_func(*args, **kwargs):

        with _database.atomic() as transaction:
            try:
                return func(db=_database, *args, **kwargs)
            except PeeweeException as pe:
                logging.error(pe)
                transaction.rollback()

    return wrap_func
