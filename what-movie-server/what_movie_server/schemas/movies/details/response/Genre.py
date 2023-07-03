from pydantic import BaseModel


class Genre(BaseModel):
    genre_id: int
    genre_name: str
