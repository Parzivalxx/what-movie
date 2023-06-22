from pydantic import BaseModel


class NoDataResponse(BaseModel):
    status: str
    message: str
