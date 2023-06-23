from pydantic import BaseModel


class ListGetRequest(BaseModel):
    user_id: int
