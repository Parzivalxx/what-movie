from pydantic import BaseModel


class Times(BaseModel):
    start_time: str
    end_time: str
