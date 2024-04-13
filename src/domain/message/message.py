from pydantic import BaseModel


class Message(BaseModel):
    title: str
    body: str
    to: str

    def __dict__(self) -> dict:
        return self.model_dump()
