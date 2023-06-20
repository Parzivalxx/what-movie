from pydantic import BaseModel, Field


class AuthSuccessPostResponse(BaseModel):
    status: str = Field(default="success")
    message: str
    auth_token: str
