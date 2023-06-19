from pydantic import BaseModel

from .ImageMedium import ImageMedium


class Still(BaseModel):
    image_orientation: str
    medium: ImageMedium
