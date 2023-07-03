from pydantic import BaseModel

from .FilmData import FilmData


class DetailsGetResponse(BaseModel):
    status: str
    data: FilmData
