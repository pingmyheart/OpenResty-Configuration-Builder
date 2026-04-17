from typing import List, Optional

from pydantic import BaseModel


class Filter(BaseModel):
    name: str
    args: dict


class Route(BaseModel):
    name: str
    location: str
    methods: Optional[List[str]] = ["GET"]
    filters: Optional[List[Filter]] = []
