from pydantic import BaseModel

from .CinemaData import CinemaData


class CinemaDetailsGetResponse(BaseModel):
    status: str
    data: CinemaData
