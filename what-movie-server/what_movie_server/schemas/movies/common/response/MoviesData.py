from pydantic import BaseModel
from typing import List

from .Film import Film
from .Status import Status


class MoviesData(BaseModel):
    films: List[Film]
    status: Status
