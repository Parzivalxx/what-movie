from pydantic import BaseModel

from ...common.response.UserSchema import UserSchema


class ReadUserSuccessGetResponse(BaseModel):
    status: str
    data: UserSchema
