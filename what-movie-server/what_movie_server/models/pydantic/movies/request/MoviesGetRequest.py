from pydantic import BaseModel, Field


class MoviesGetRequest(BaseModel):
    n: int = Field(default=10)
