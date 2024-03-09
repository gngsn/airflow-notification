from unittest import TestCase

import pendulum

from src.persistence.base import init_db
from src.persistence.model.meeting import Meeting
from src.persistence.model.user import User


class TestUser(TestCase):

    def test_session(self):
        def new_user():
            u = User.create(name="test_4")
            print('new user id : ', u)

        def error():
            raise ValueError("냠")

        def new_meeting():
            m = Meeting.create(
                owner="test_4",
                name="스크럼 회의 1",
                room="F11R01",
                start_time=pendulum.now().subtract(hours=1),
                end_time=pendulum.now().add(days=1)
            )

            print('new meeting id : ', m)

        def exec():
            new_user()
            # error()
            new_meeting()

        init_db()
        exec()
