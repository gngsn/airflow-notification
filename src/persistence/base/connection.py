__all__ = ['init_pg', 'init_sqlite', 'database_', 'execute', 'BaseModel']

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

    def __init__(self, host: str, db_name: str, db_port: int, username: str, password: str):
        self.__property__ = {
            'db_name': db_name,
            'user': username,
            'password': password,
            'host': host,
            'port': db_port
        }

    def __enter__(self):
        self.__connection__ = PostgresqlDatabase(
            self.__property__['db_name'],
            user=self.__property__['user'],
            password=self.__property__['password'],
            host=self.__property__['host'],
            port=self.__property__['db_port']
        )

    def __exit__(self):
        self.__connection__.close()
