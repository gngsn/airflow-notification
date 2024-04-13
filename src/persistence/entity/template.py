from peewee import CharField

from src.persistence.base.connection import BaseModel


class MessageTemplate(BaseModel):
    """ Messages template """

    class Meta:
        table_name = 'message_template'

    id: str = CharField(primary_key=True, max_length=50)
    title: str = CharField(max_length=1000)
    message: str = CharField(max_length=1000)

    @classmethod
    def find_all(cls):
        return cls.select()
