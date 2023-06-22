from pydantic import BaseModel

from .ImageMedium import ImageMedium


class Poster(BaseModel):
    image_orientation: str
    region: str
    medium: ImageMedium
