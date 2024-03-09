from pydantic import BaseModel

from src.lib.hash import hash_md5


class MessageSchema(BaseModel):
    """Message schema."""

    id: str
    schedule: str
    args: dict[str, str]
    checksum: str


def message_schema(id, schedule, args):
    """ Message schema factory method """

    return MessageSchema(
        id=id,
        schedule=schedule,
        args=args,
        checksum=hash_md5(id, schedule, args)
    )


SCHEMAS = [
    message_schema(
        id="UMSV10001",
        schedule="*/30 9-18 * * MON,TUE,WED,THU,FRI",
        args={"task_count": "SELECT count(*) AS task_count FROM TODO ..."},
        target="SELECT u.id AS target FROM users u, meeting m WHERE id = $1",
    ),
    message_schema(
        id="UMSV10002",
        schedule="*/30 9-18 * * MON,TUE,WED,THU,FRI",
        args={"task_count": "SELECT count(*) AS task_count FROM TODO ..."}
    ),
]
