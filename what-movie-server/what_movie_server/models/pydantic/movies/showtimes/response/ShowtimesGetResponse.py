from pydantic import BaseModel
from typing import List

from .Film import Film
from .Cinema import Cinema
from ...common.response.Status import Status


class ShowtimesGetResponse(BaseModel):
    film: Film
    cinemas: List[Cinema]
    status: Status
