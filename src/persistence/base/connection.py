__all__ = ['init_pg', 'init_sqlite', 'database_', 'execute', 'BaseModel']

from peewee import PostgresqlDatabase, Model, SqliteDatabase, Proxy

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
    host: str
    db_name: str
    db_schema: str
    username: str
    password: str

    def __init__(self, host: str, db_name: str, db_schema: str, username: str, password: str):
        self.host = host
        self.db_name = db_name
        self.db_schema = db_schema
        self.username = username
        self.password = password
