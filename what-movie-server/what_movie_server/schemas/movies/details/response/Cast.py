from pydantic import BaseModel


class Cast(BaseModel):
    cast_id: int
    cast_name: str
