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
