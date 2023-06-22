from pydantic import BaseModel, HttpUrl


class AgeRating(BaseModel):
    rating: str
    age_rating_image: HttpUrl
    age_advisory: str
