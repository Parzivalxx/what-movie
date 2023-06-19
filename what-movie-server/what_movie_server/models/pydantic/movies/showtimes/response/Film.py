from pydantic import BaseModel, HttpUrl
from typing import List, Dict

from ...common.response.AgeRating import AgeRating


class Film(BaseModel):
    film_id: int
    imdb_id: int
    imdb_title_id: str
    film_name: str
    other_titles: Dict[str, str]
    version_type: str
    age_rating: List[AgeRating]
    film_image: HttpUrl
    film_image_height: int
    film_image_width: int
