from pydantic import BaseModel


class Producer(BaseModel):
    producer_id: int
    producer_name: str
