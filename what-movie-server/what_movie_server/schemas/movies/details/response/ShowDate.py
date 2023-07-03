from pydantic import BaseModel


class ShowDate(BaseModel):
    date: str
