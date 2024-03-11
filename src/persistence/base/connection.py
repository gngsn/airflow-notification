__all__ = ['init_pg', 'init_sqlite', 'database_', 'execute']

from peewee import PostgresqlDatabase, Proxy, Model, Database, SqliteDatabase

database_ = Proxy()


def init_db(initializer: callable, db: Database):
    """ Lazy Initialize Database Connection """
    initializer(db)


def init_pg(url="postgresql://postgres:postgres@localhost/postgres") -> None:
    """Initialize PostgreSQL database."""
    init_db(database_.initialize, PostgresqlDatabase(url))


def init_sqlite(url=":memory:") -> None:
    """Initialize PostgreSQL database."""
    init_db(database_.initialize, SqliteDatabase(url))


def execute(sql):
    return database_.execute_sql(sql)


class BaseModel(Model):
    class Meta:
        database = database_
