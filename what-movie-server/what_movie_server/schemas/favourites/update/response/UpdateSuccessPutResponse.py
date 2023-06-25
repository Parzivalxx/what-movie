from pydantic import BaseModel

from ...common.response.withdata.Favourite import Favourite


class UpdateSuccessPutResponse(BaseModel):
    status: str
    data: Favourite
