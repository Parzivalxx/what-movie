from pydantic import BaseModel
from typing import Optional, List

from .ShowDate import ShowDate
from .Status import Status


class CinemaData(BaseModel):
    cinema_id: int
    cinema_name: str
    address: str
    address2: str
    city: str
    county: str
    country: str
    postcode: str
    phone: str
    lat: float
    lng: float
    distance: float
    ticketing: int
    directions: str
    logo_url: str
    show_dates: Optional[List[ShowDate]]
    status: Status
