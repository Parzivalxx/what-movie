from pydantic import BaseModel, HttpUrl


class ImageMedium(BaseModel):
    film_image: HttpUrl
    width: int
    height: int
