from pydantic import BaseModel, ConfigDict


class PhoneBase(BaseModel):
    number: str

    model_config = ConfigDict(from_attributes=True)


class PhoneCreate(PhoneBase):
    organization_id: int


class PhoneRead(PhoneBase):
    id: int