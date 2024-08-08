from src.persistence.base import init_pg
from src.persistence.base.connection import database_
from src.persistence.entity.schema import MessageSchema
from src.persistence.entity.template import MessageTemplate

init_pg()


def messages_templates():
    templates = {
        "id": "UMSV10001",
        "title": "이번 주 회의 건 수",
        "message": "이번 주 $meeting_name 회의가 예정되어 있어요. $remaining 시간 남았어요.",
    }, {
        "id": "UMSV10002",
        "title": "새로운 회의",
        "message": "새로운 회의가 있습니다.\n 담당자: $owner | 시간: $time",
    }, {
        "id": "UMSV10003",
        "title": "회의 시작 10분 전",
        "message": "$meeting_name 회의가 10분 뒤에 $location에서 진행돼요.",
    }

    database_.create_tables([MessageTemplate])

    for template in templates:
        MessageTemplate.create(**template)


def messages_schema():
    schemas = [{
        "template_id": "UMSV10001",
        "title": "이번 주 회의 건 수",
        "schedule": '* * * * *',
        "args": '{}',
        "target": "SELECT u.id AS target, m.name AS meeting_name, m.end_time, (m.end_time - now())::time as remaining FROM users u join meeting m on u.id = m.host and m.start_time >= '2024-04-09'::date and m.end_time <= '2024-04-09'::date + interval '5 days'",
        "check_keys": 'target',
    }]
    database_.create_tables([MessageSchema])

    for schema in schemas:
        MessageSchema.create(**schema)


if __name__ == "__main__":
    messages_schema()
