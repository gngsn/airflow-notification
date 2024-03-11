from airflow.decorators import dag, task
from pendulum import datetime


@dag(
    start_date=datetime(2021, 1, 1),
    schedule_interval="*/30 * * * *",
    catchup=False,
)
def trigger():
    @task.virtualenv(
        task_id="generator",
        system_site_packages=False,
        python_version='3.11',
        requirements=[
            "peewee==3.17.0",
            "pendulum==2.1.2",
            "pydantic==2.6.0",
            "croniter",
            "psycopg2-binary",
        ],
    )
    def generator():
        from croniter import croniter
        from string import Template

        import pendulum

        from src.domain.message import SCHEMAS, TEMPLATES, MessageSchema
        from src.persistence.base import init_pg
        from src.persistence.base import execute, transactional

        def to_json(cursor):
            for row in cursor.fetchall():
                yield {column[0]: value for column, value in zip(cursor.description, row)}

        @transactional
        def get_targets(schema: MessageSchema) -> list[dict]:
            cursor = execute(schema.target)
            table = list(to_json(cursor))
            return table

        def match(schedule, now=pendulum.now(tz="Asia/Seoul")) -> bool:
            return croniter.match(schedule, now)

        def replace(_templates, target):
            return Template(_templates.message).substitute(**target)

        init_pg()

        messages = []
        for s in SCHEMAS:
            if match(s.schedule):
                """ Messages scheduled now """
                for args in get_targets(s):
                    matched_messages_iter = filter(lambda t: t.id == s.id, TEMPLATES)
                    message_templates = next(matched_messages_iter)
                    substitute = replace(message_templates, args)

                    messages.append(substitute)

        return messages

    @task
    def send(schema: list[str]):
        if schema is None:
            return "Error"

        return schema

    schema = generator()
    send(schema)


trigger_dag = trigger()

if __name__ == "__main__":
    trigger_dag.test()
