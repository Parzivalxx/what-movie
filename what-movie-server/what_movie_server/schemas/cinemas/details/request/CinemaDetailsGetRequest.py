from pydantic import BaseModel


class CinemaDetailsGetRequest(BaseModel):
    cinema_id: str
