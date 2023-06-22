from pydantic import BaseModel, HttpUrl
from typing import Dict

from .Showings import Showings


class Cinema(BaseModel):
    cinema_id: int
    cinema_name: str
    distance: float
    logo_url: HttpUrl
    showings: Dict[str, Showings]
