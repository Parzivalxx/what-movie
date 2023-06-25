from pydantic import BaseModel
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    email: str
    password: str
    registered_on: datetime
    admin: bool

    class Config:
        orm_mode = True
