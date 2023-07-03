from pydantic import BaseModel


class Director(BaseModel):
    director_id: int
    director_name: str
