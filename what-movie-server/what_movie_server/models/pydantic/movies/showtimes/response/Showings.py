from pydantic import BaseModel
from typing import List

from .Times import Times


class Showings(BaseModel):
    film_id: int
    film_name: str
    times: List[Times]
