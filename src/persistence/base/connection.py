__all__ = ['Connector', 'init_pg', 'init_sqlite', 'database_', 'execute', 'BaseModel']

import traceback

from peewee import PostgresqlDatabase, Model, SqliteDatabase, Proxy, Database

database_ = Proxy()


def init_pg(url="postgresql://postgres:postgres@localhost/ums") -> None:
    """Initialize PostgreSQL database."""
    database_.initialize(PostgresqlDatabase(url))


def init_sqlite(url=":memory:") -> None:
    """Initialize Sqlite database."""
    database_.initialize(SqliteDatabase(url))


def execute(sql):
    return database_.execute_sql(sql)


class BaseModel(Model):
    class Meta:
        database = database_


class Connector:
    __property__: dict
    __connection__: Database = None

    def __init__(self, connection):
        self.__property__ = {
            'db_name': connection.database,
            'user': connection.username,
            'password': connection.password,
            'host': connection.host,
            'port': connection.port
        }

    def __enter__(self):
        self.__connection__ = PostgresqlDatabase(
            self.__property__['db_name'],
            user=self.__property__['user'],
            password=self.__property__['password'],
            host=self.__property__['host'],
            port=self.__property__['port']
        )

    def __exit__(self, exc_type, exc_value, tb):
        """ https://docs.python.org/3/reference/datamodel.html#object.__exit__"""
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

        self.__connection__.close()
