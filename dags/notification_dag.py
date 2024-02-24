import pendulum
from airflow.decorators import dag, task


@task()
def generator():
    return {
        "id": 0,
        "schedule": "*/30 9-18 * * MON,TUE,WED,THU,FRI",
        "template_id": "UMSV10001",
        "argument": {
            "task_count": "select count(*) as task_count from TODO ..."
        },
        "argument_valid": [
            "task_count"
        ]
    }


@task
def send(schema):
    messages = [
        {
            "template_id": "UMSV10001",
            "title": "이번 주 회의 건 수",
            "content": "이번 주 {{task_count}}개의 회의가 예정되어 있어요."
        },
        {
            "template_id": "UMSV10002",
            "title": "새로운 회의",
            "content": "새로운 회의가 있습니다.\n 담당자: {{owner}} | 시간: {{time}}"
        },
        {
            "template_id": "UMSV10003",
            "title": "회의 시작 10분 전",
            "content": "{{meeting_name}} 회의가 10분 뒤에 {{location}}에서 실행돼요."
        },
    ]

    if schema is None:
        return "Error"

    return [d for d in messages if d["template_id"] == schema["template_id"]]


@dag(
    start_date=pendulum.datetime(2021, 1, 1, tz="Asia/Seoul"),
    schedule_interval="*/30 * * * *",
    catchup=False,
)
def trigger():
    schema = generator()
    send(schema)


trigger_dag = trigger()

if __name__ == "__main__":
    trigger_dag.test()
