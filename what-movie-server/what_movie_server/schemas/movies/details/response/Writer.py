from pydantic import BaseModel


class Writer(BaseModel):
    writer_id: int
    writer_name: str
