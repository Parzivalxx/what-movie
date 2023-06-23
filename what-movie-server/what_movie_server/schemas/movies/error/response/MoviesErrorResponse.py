from pydantic import BaseModel


class MoviesErrorResponse(BaseModel):
    status: str
    message: str
