from pydantic import BaseModel


class FavouritePayloadRequest(BaseModel):
    user_id: int
    film_id: int
    cinema_id: int
    start_time: str
    end_time: str
    is_3d: bool
