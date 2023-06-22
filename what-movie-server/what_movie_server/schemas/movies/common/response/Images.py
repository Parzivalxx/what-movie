from pydantic import BaseModel
from typing import Optional, Dict

from .Poster import Poster
from .Still import Still


class Images(BaseModel):
    poster: Optional[Dict[str, Poster]]
    still: Optional[Dict[str, Still]]
