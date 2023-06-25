from pydantic import BaseModel


class DeleteUserSuccessDeleteResponse(BaseModel):
    status: str
    message: str
