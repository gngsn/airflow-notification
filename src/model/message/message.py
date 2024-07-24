from pydantic import BaseModel


class Message(BaseModel):
    title: str
    body: str
    to: str
