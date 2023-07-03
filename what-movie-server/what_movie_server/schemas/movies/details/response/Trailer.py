from pydantic import BaseModel


class Trailer(BaseModel):
    film_trailer: str
    trailer_image: str
    version: int
    quality: str
    region: str
