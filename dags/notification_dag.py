from airflow.decorators import dag, task
from pendulum import datetime


@dag(
    start_date=datetime(2021, 1, 1),
    schedule="*/30 * * * *",
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
    def run():
        from src.domain.message import generator
        from src.domain.message import sender
        from src.domain.message_queue import MessageQueue

        MessageQueue()

        generator.run()
        sender.run()

    run()


trigger_dag = trigger()

if __name__ == "__main__":
    trigger_dag.test()
