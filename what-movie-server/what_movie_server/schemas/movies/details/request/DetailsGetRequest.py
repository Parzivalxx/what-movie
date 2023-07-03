from pydantic import BaseModel


class DetailsGetRequest(BaseModel):
    film_id: str
