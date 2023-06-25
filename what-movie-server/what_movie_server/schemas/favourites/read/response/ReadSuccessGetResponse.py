from pydantic import BaseModel

from ...common.response.withdata.Favourite import Favourite


class ReadSuccessGetResponse(BaseModel):
    status: str
    data: Favourite
