from unittest import TestCase

import pendulum
from sqlalchemy import select

from src.model.database.base import transactional
from src.model.database.meeting import Meeting
from src.model.database.user import User


class TestUser(TestCase):

    def test_session(self):
        def new_user(db_session):
            db_session.add(User(name="test_2"))

        def error():
            raise ValueError("냠")

        def new_meeting(db_session):
            db_session.add(
                Meeting(
                    owner="test_1",
                    room="F11R01",
                    start_time=pendulum.now(),
                    end_time=pendulum.now()
                ))

        def select_user(db_session, id=1):
            stmt = select(User).where(User.id == id)
            print('result111 : ', db_session.execute(stmt).first())

        @transactional
        def exec(db_session):
            new_user(db_session)
            select_user(db_session, 2)

            new_meeting(db_session)
            select_user(db_session, 2)

        exec()
