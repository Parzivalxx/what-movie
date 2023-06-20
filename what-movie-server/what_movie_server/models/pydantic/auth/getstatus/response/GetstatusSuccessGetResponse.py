from pydantic import BaseModel, Field

from .Data import Data


class GetstatusSuccessGetResponse(BaseModel):
    status: str = Field(default="success")
    data: Data
