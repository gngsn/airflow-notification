import pendulum
from airflow.decorators import dag, task
from croniter import croniter
from sqlalchemy import Engine

from src.domain.const import *
from src.domain.message.schema import SCHEMAS
from src.domain.message.template import TEMPLATES
from src.model.database.base import transactional


@dag(
    start_date=pendulum.datetime(2021, 1, 1, tz="Asia/Seoul"),
    schedule_interval="*/30 * * * *",
    catchup=False,
)
def trigger():
    @task
    def generator():
        def match(schedule, now=pendulum.now(tz="Asia/Seoul")) -> bool:
            return croniter.match(schedule, now)

        connect = Engine.connect()

        for s in SCHEMAS:
            if match(s.schedule):
                _templates = filter(lambda t: t.id == s.id, TEMPLATES[s])

                for template in _templates:
                    get_targets(connect, template)

        return {
            TEMPLATE_ID: "UMSV10001",
            TEMPLATE_KEY_SCHEDULE: "*/30 9-18 * * MON,TUE,WED,THU,FRI",
            TEMPLATE_KEY_ARGS: {"task_count": "select count(*) as task_count from TODO ..."},
            TEMPLATE_KEY_CHECKSUM: "task_count",
        }

    @transactional
    def get_targets(connect, template):
        with connect:
            rs = connect.execute(template.target)

            for row in rs:
                print(row)

    @task
    def send(schema: dict):
        messages = [
            {
                TEMPLATE_ID: "UMSV10001",
                MESSAGE_TITLE: "이번 주 회의 건 수",
                MESSAGE_CONTENT: "이번 주 {{task_count}}개의 회의가 예정되어 있어요.",
            },
            {
                TEMPLATE_ID: "UMSV10002",
                MESSAGE_TITLE: "새로운 회의",
                MESSAGE_CONTENT: "새로운 회의가 있습니다.\n 담당자: {{owner}} | 시간: {{time}}",
            },
            {
                TEMPLATE_ID: "UMSV10003",
                MESSAGE_TITLE: "회의 시작 10분 전",
                MESSAGE_CONTENT: "{{meeting_name}} 회의가 10분 뒤에 {{location}}에서 실행돼요.",
            },
        ]

        if schema is None:
            return "Error"

        return [d for d in messages if d["template_id"] == schema["template_id"]]

    schema = generator()
    send(schema)


trigger_dag = trigger()

if __name__ == "__main__":
    trigger_dag.test()
