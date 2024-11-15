from datetime import datetime

from pydantic import BaseModel, PositiveInt


class UserTest(BaseModel):
    id: int
    name: str = "John Doe"
    signup_at: datetime | None
    tastes: dict[str, PositiveInt]


def test_user_creation():
    external_data = {
        "id": 123,
        "signup_at": "2019-06-01 12:22",
        "tastes": {
            "wine": 9,
            b"cheese": 7,
            "cabbage": "1",
        },
    }

    user = User(**external_data)
    print(user.id)
    print(user.model_dump())
