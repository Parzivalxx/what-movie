from pydantic import BaseModel, Field


class LogoutSuccessPostResponse(BaseModel):
    status: str = Field(default="success")
    message: str
