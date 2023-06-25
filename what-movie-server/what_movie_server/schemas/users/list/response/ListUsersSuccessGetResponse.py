from pydantic import BaseModel
from typing import List

from ...common.response.UserSchema import UserSchema


class ListUsersSuccessGetResponse(BaseModel):
    status: str
    data: List[UserSchema]
