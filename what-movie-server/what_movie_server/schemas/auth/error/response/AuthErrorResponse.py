from pydantic import BaseModel, Field


class AuthErrorResponse(BaseModel):
    status: str = Field(default="fail")
    message: str
