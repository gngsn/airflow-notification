from peewee import CharField, AutoField
from playhouse.postgres_ext import JSONField

from src.persistence.base.connection import BaseModel


class MessageSchema(BaseModel):
    """Message schema DB Model."""

    class Meta:
        table_name = 'message_schema'

    id: str = AutoField(primary_key=True)
    template_id: str = CharField(max_length=50)
    schedule: str = CharField(max_length=255)
    args: dict = JSONField(default={})

    target_db: str = CharField()
    target_items: str = CharField()
    target_users: str = CharField()

    checksum_keys: str = CharField(max_length=255)

    @classmethod
    def select_all(cls):
        return cls.select()

    def get_targets(self):
        return self.target_items

# if __name__ == "__main__":
#     from src.persistence.base import init_pg
#     from string import Template
#
#
#     def to_json(cursor):
#         for row in cursor.fetchall():
#             yield {column[0]: value for column, value in zip(cursor.description, row)}
#
#
#     init_pg()
#
#     _templates = MessageTemplate(
#         id="UMSV10001",
#         title="이번 주 회의 건 수",
#         message="이번 주 ${meeting_name} 회의가 예정되어 있어요. ${remaining} 시간 남았어요.",
#     )
#
#     for s in MessageSchema.select_all():
#         for target in s.get_targets():
#             substitute = Template(_templates.message).substitute(**target)
#             print(substitute)
