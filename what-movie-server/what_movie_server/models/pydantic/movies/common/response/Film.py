from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict

from .ReleaseDate import ReleaseDate
from .AgeRating import AgeRating
from .Images import Images


class Film(BaseModel):
    film_id: int
    imdb_id: int
    imdb_title_id: str
    film_name: str
    other_titles: Dict[str, str]
    release_dates: List[ReleaseDate]
    age_rating: List[AgeRating]
    film_trailer: HttpUrl
    synopsis_long: str
    images: Optional[Images]
