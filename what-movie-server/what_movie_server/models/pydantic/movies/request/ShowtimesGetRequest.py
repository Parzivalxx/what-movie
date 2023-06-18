from pydantic import BaseModel, Field


class ShowtimesGetRequest(BaseModel):
    film_id: int
    date: str
    n: int = Field(default=10)
