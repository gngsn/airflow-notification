from pydantic import BaseModel


class MessagesTemplate(BaseModel):
    """ Messages template """

    id: str
    title: str
    message: str


TEMPLATES = [
    MessagesTemplate(
        id="UMSV10001",
        title="이번 주 회의 건 수",
        message="이번 주 $meeting_name 회의가 예정되어 있어요. $remaining 시간 남았어요.",
    ),
    MessagesTemplate(
        id="UMSV10002",
        title="새로운 회의",
        message="새로운 회의가 있습니다.\n 담당자: {{owner}} | 시간: {{time}}",
    ),
    MessagesTemplate(
        id="UMSV10003",
        title="회의 시작 10분 전",
        message="{{meeting_name}} 회의가 10분 뒤에 {{location}}에서 실행돼요.",
    ),
]
