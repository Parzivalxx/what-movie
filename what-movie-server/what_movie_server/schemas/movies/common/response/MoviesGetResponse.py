from pydantic import BaseModel
from typing import Optional

from .MoviesData import MoviesData


class MoviesGetResponse(BaseModel):
    status: str
    data: Optional[MoviesData]
