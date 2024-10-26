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
        python_version='3.12',
        requirements=[
            "peewee==3.17.0",
            "pendulum==2.1.2",
            "psycopg2-binary",
        ],
    )
    def pre_setup():
        from pendulum import now
        from src.persistence import init_pg
        from src.persistence.queue import NotificationQueue

        init_pg()

        now_date = now().date()
        NotificationQueue.create_partition_if_not_exists(now_date)

    @task.virtualenv(
        task_id="generate",
        system_site_packages=False,
        python_version='3.12',
        requirements=[
            "peewee==3.17.0",
            "pendulum==2.1.2",
            "pydantic==2.6.0",
            "croniter",
            # "psycopg2-binary",
        ],
    )
    def generate():
        from pendulum import now
        from src.persistence import init_pg
        from src.persistence.queue import NotificationQueue

        init_pg()

        now_date = now().date()
        NotificationQueue.create_partition_if_not_exists(now_date)

        from src.model.message import generator

        generator.run()

    @task.virtualenv(
        task_id="send",
        system_site_packages=False,
        python_version='3.12',
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
        from src.model.message.sender import ConsoleSender

        init_pg()
        sender.run([ConsoleSender()])

    pre_setup() >> generate() >> send()


trigger_dag = trigger()

if __name__ == "__main__":
    # get_task = trigger_dag.get_task('generate')
    # get_task.run()
    trigger_dag.test()
