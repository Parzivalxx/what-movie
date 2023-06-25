from pydantic import BaseModel
from typing import List

from ...common.response.withdata.Favourite import Favourite


class ListSuccessGetResponse(BaseModel):
    status: str
    data: List[Favourite]
