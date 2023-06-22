from pydantic import BaseModel, Extra


class AuthHeaders(BaseModel):
    Authorization: str

    class Config:
        extra = Extra.allow
