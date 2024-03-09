from unittest import TestCase

import pendulum

from src.model.database.base import init_db
from src.model.database.meeting import Meeting
from src.model.database.user import User


class TestUser(TestCase):

    def test_session(self):
        def new_user():
            u = User.create(name="test_2")
            print('new user id : ', u)

        def error():
            raise ValueError("냠")

        def new_meeting():
            m = Meeting.create(
                owner="test_2",
                room="F11R01",
                start_time=pendulum.now(),
                end_time=pendulum.now()
            )

            print('new meeting id : ', m)

        def exec():
            new_user()
            error()
            new_meeting()

        init_db()
        exec()
