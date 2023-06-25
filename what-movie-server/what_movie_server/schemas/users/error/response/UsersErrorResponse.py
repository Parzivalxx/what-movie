from pydantic import BaseModel


class UsersErrorResponse(BaseModel):
    status: str
    message: str
