from pydantic import BaseModel
from typing import List, Dict, Optional

from ...common.response.AgeRating import AgeRating
from ...common.response.Images import Images


class Film(BaseModel):
    film_id: int
    imdb_id: int
    imdb_title_id: str
    film_name: str
    other_titles: Optional[Dict[str, str]]
    version_type: str
    age_rating: List[AgeRating]
    images: Images
