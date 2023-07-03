from pydantic import BaseModel
from datetime import datetime


class Data(BaseModel):
    user_id: str
    email: str
    admin: bool
    added_on: datetime
