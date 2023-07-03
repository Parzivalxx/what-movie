from pydantic import BaseModel
from datetime import datetime


class Favourite(BaseModel):
    id: int
    user_id: int
    film_id: int
    cinema_id: int
    start_time: str
    end_time: str
    cinema_type: str
    added_on: datetime

    class Config:
        orm_mode = True
