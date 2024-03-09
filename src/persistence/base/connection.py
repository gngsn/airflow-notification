__all__ = ['init_db', 'database_', 'execute']

from peewee import PostgresqlDatabase, Proxy, Model

database_ = Proxy()


def init_db(url="postgresql://postgres:postgres@localhost/postgres"):
    """ Lazy Initialize Database Connection """
    database_.initialize(PostgresqlDatabase(url))


def execute(sql):
    return database_.execute_sql(sql)


class BaseModel(Model):
    class Meta:
        database = database_
