__all__ = ['transactional', 'tx_db']

import logging
from functools import wraps

from peewee import PeeweeException

from src.persistence.base import database_


def transactional(func):
    """ transactional decorator.
        use transaction by annotating @transactional decorator to method
    """

    @wraps(func)
    def wrap_func(*args, **kwargs):

        with database_.atomic() as transaction:
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

        with database_.atomic() as transaction:
            try:
                return func(database=database_, *args, **kwargs)
            except PeeweeException as pe:
                logging.error(pe)
                transaction.rollback()

    return wrap_func
