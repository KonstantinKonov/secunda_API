from typing import List
from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    name: str
    parent_id: int | None

    model_config = ConfigDict(from_attributes=True)


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    children: List["ActivityRead"] = []


from pydantic import TypeAdapter
ActivityRead.model_rebuild()