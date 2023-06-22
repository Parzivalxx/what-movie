from pydantic import BaseModel
from typing import Optional


class Status(BaseModel):
    count: int
    state: str
    method: str
    message: Optional[str]
    request_method: str
    version: str
    territory: str
    device_datetime_sent: str
    device_datetime_used: str
