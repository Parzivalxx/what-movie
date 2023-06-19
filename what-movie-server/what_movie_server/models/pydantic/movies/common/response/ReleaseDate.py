from pydantic import BaseModel


class ReleaseDate(BaseModel):
    release_date: str
    notes: str
