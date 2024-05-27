from peewee import CharField

from src.persistence.base.connection import BaseModel, database_, init_pg


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


if __name__ == "__main__":
    init_pg()
    database_.create_tables([MessageTemplate])
