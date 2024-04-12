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
    def generate():
        from src.domain.message import generator

        return generator.run()

    @task
    def send(schema: list[str]):
        if schema is None:
            return "Error"

        return schema

    messages = generate()
    send(messages)


trigger_dag = trigger()

if __name__ == "__main__":
    trigger_dag.test()
