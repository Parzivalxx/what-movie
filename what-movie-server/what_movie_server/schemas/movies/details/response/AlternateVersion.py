from pydantic import BaseModel


class AlternateVersion(BaseModel):
    film_id: int
    film_name: str
    version_type: str
