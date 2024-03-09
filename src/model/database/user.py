from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.sql.ddl import CreateSequence

from src.model.database.base import Base


class User(Base):
    """ User DB Model """
    __tablename__ = "users"

    id: int = Column(Integer, Sequence('users_id_seq'), primary_key=True, autoincrement=True)
    name: str = Column(String)


if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import postgresql

    ddl_users = CreateTable(User.__table__).compile(dialect=postgresql.dialect())
    ddl_users_seq = CreateSequence(User.__table__)
    print(ddl_users)
    print(ddl_users_seq)
