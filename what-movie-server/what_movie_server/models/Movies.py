from pydantic import BaseModel, Field


class MoviesRequest(BaseModel):
    n: int = Field(default=10)


class ShowtimesRequest(BaseModel):
    film_id: int
    date: str
    n: int = Field(default=10)
