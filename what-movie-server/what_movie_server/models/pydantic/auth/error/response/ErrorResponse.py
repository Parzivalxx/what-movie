from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    status: str = Field(default="fail")
    message: str
