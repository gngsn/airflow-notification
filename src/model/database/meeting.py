from sqlalchemy import Column, String, text, DateTime, Integer

from src.model.database.base import Base


class Meeting(Base):
    """ Meeting DB Model """
    __tablename__ = "meeting"

    id: int = Column(Integer, primary_key=True)
    room: str = Column(String)
    owner: str = Column(String)
    start_time: DateTime = Column(DateTime, server_default=text('NOW()'))
    end_time: DateTime = Column(DateTime, server_default=text('NOW()'))
    # participants: str # TODO


if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import postgresql

    ddl_meeting = CreateTable(Meeting.__table__).compile(dialect=postgresql.dialect())
    print(ddl_meeting)
