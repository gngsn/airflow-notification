from pydantic import BaseModel

from src.domain.message.template import MessagesTemplate
from src.lib.hash import hash_md5


class MessageSchema(BaseModel):
    """Message schema."""

    id: str
    schedule: str
    args: dict[str, str]
    target: str
    checksum: str


def message_schema(id, schedule, args, target):
    """ Message schema factory method """

    return MessageSchema(
        id=id,
        schedule=schedule,
        args=args,
        target=target,
        checksum=hash_md5(''.join([id]))
    )


SCHEMAS = [
    message_schema(
        id="UMSV10001",
        schedule="* * * * *",
        # schedule="*/30 9-18 * * MON,TUE,WED,THU,FRI",
        args={},
        target="SELECT u.id AS target, m.name AS meeting_name, (m.end_time - now())::time as remaining FROM users u join meeting m on u.name = m.owner WHERE m.start_time <= now() and m.end_time >= now()",
    )
    # ,
    # message_schema(
    #     id="UMSV10002",
    #     schedule="*/30 9-18 * * MON,TUE,WED,THU,FRI",
    #     target="SELECT null",
    #     args={}
    # )
]

from string import Template

if __name__ == "__main__":
    from src.persistence.base import init_pg, execute


    def get_targets(template):
        cursor = execute(template.target)
        table = list(to_json(cursor))
        print(table)
        return table


    def to_json(cursor):
        for row in cursor.fetchall():
            yield {column[0]: value for column, value in zip(cursor.description, row)}


    init_pg()

    _templates = MessagesTemplate(
        id="UMSV10001",
        title="이번 주 회의 건 수",
        message="이번 주 ${meeting_name} 회의가 예정되어 있어요. ${remaining} 시간 남았어요.",
    ).__dict__

    for s in SCHEMAS:
        for target in get_targets(s):
            substitute = Template(_templates['message']).substitute(**target)
            print(substitute)
