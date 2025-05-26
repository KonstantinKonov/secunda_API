from pydantic import BaseModel, ConfigDict


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int