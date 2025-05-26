from src.models import Building, Activity, Organization
from src.schemas import OrganizationRead, BuildingRead, ActivityRead
from src.repositories.mappers.base import DataMapper


class OrganizationMapper(DataMapper[Organization, OrganizationRead]):
    @classmethod
    def map_to_domain_entity(cls, model: Organization) -> OrganizationRead:
        return OrganizationRead.model_validate(model)
    
    @classmethod
    def map_to_orm_entity(cls, dto: OrganizationRead) -> Organization:
        return Organization(**dto.model_dump())


class BuildingMapper(DataMapper[Building, BuildingRead]):
    @classmethod
    def map_to_domain_entity(cls, model: Building) -> BuildingRead:
        return BuildingRead.model_validate(model)

    @classmethod
    def map_to_orm_entity(cls, dto: BuildingRead) -> Building:
        return Building(**dto.model_dump())


class ActivityMapper(DataMapper[Activity, ActivityRead]):
    @classmethod
    def map_to_domain_entity(cls, model: Activity) -> ActivityRead:
        return ActivityRead.model_validate(model)

    @classmethod
    def map_to_orm_entity(cls, dto: ActivityRead) -> Activity:
        return Activity(**dto.model_dump())
