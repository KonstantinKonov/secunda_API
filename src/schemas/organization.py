from typing import List
from pydantic import BaseModel, ConfigDict
from src.schemas.phone import PhoneRead
from src.schemas.building import BuildingRead
from src.schemas.activity import ActivityRead


class OrganizationBase(BaseModel):
    name: str
    building_id: int

    model_config = ConfigDict(from_attributes=True)


class OrganizationCreate(OrganizationBase):
    phone_numbers: List[str] = []
    activity_ids: List[int] = []


class OrganizationRead(OrganizationBase):
    id: int
    phones: List[PhoneRead] = []
    building: BuildingRead
    activities: List[ActivityRead] = []


from src.schemas.phone import PhoneRead
from src.schemas.building import BuildingRead
from src.schemas.activity import ActivityRead
OrganizationRead.model_rebuild()