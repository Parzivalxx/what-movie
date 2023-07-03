from pydantic import BaseModel
from typing import Optional, List, Dict

from ...common.response.ReleaseDate import ReleaseDate
from ...common.response.AgeRating import AgeRating
from ...common.response.Images import Images
from ...common.response.Status import Status
from .Trailer import Trailer
from .Genre import Genre
from .Cast import Cast
from .Director import Director
from .Producer import Producer
from .Writer import Writer
from .ShowDate import ShowDate
from .AlternateVersion import AlternateVersion


class FilmData(BaseModel):
    film_id: int
    imdb_id: int
    imdb_title_id: str
    film_name: str
    other_titles: Optional[Dict[str, str]]
    version_type: str
    images: Optional[Images]
    synopsis_long: str
    distributor_id: int
    distributor: str
    release_dates: List[ReleaseDate]
    age_rating: List[AgeRating]
    duration_mins: int
    review_stars: int
    review_txt: str
    trailers: Optional[Dict[str, List[Trailer]]]
    genres: List[Genre]
    cast: List[Cast]
    directors: List[Director]
    producers: List[Producer]
    writers: List[Writer]
    show_dates: Optional[List[ShowDate]]
    alternate_versions: Optional[List[AlternateVersion]]
    status: Status
