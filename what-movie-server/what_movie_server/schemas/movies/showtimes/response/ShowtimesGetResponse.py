from pydantic import BaseModel
from typing import Optional

from .ShowtimesData import ShowtimesData


class ShowtimesGetResponse(BaseModel):
    status: str
    data: Optional[ShowtimesData]
