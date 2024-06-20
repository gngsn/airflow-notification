from peewee import CharField, IntegerField

from src.persistence.base.connection import BaseModel


class ExternalDbConnection(BaseModel):
    """External DB Connection Model."""

    class Meta:
        table_name = 'external_db_connection'

    id: str = CharField(primary_key=True)
    host: str = CharField(max_length=255)
    database: str = CharField(max_length=100)
    port: int = IntegerField()
    username: str = CharField(max_length=100)
    password: str = CharField(max_length=255)

    @classmethod
    def select_all(cls):
        return cls.select()
