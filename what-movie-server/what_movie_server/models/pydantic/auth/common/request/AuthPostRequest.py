from pydantic import BaseModel


class AuthPostRequest(BaseModel):
    email: str
    password: str
