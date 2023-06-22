from pydantic import BaseModel


class FavouritesErrorResponse(BaseModel):
    status: str
    message: str
