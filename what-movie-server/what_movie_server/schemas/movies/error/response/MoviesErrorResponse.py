from pydantic import BaseModel


class MoviesErrorResponse(BaseModel):
    message: str
