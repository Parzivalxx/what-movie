from pydantic import BaseModel
from typing import Union, List

from .Favourite import Favourite


class WithDataResponse(BaseModel):
    status: str
    message: str
    data: Union[List[Favourite], Favourite]
