from airflow.decorators import dag, task
from pendulum import datetime


@dag(
    dag_id="notification",
    start_date=datetime(2021, 1, 1),
    schedule="*/30 * * * *",
    catchup=False,
)
def trigger():
    @task.virtualenv(
        task_id="preset_db",
        system_site_packages=False,
        python_version='3.11',
        requirements=[
            "peewee==3.17.0",
            "pendulum==2.1.2",
            "psycopg2-binary",
        ],
    )
    def preset_db():
        from pendulum import now
        from src.persistence.queue import create_partition_if_not_exists

        from src.persistence import init_pg

        init_pg()

        now_date = now().date()
        create_partition_if_not_exists(now_date)

    @task.virtualenv(
        task_id="generate",
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
        from src.model.message import generator

        generator.run()

    @task.virtualenv(
        task_id="send",
        system_site_packages=False,
        python_version='3.11',
        requirements=[
            "peewee==3.17.0",
            "pendulum==2.1.2",
            "pydantic==2.6.0",
            "psycopg2-binary",
        ],
    )
    def send():
        from src.model.message import sender
        from src.persistence import init_pg

        init_pg()
        sender.run()

    preset_db()
    generate()
    send()


trigger_dag = trigger()

if __name__ == "__main__":
    trigger_dag.test()
