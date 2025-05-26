from typing import List
from fastapi import HTTPException

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.models import Organization, OrganizationActivity, Phone, Activity
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import OrganizationMapper
from src.schemas.organization import OrganizationCreate, OrganizationRead


class OrganizationRepository(BaseRepository):
    model = Organization
    mapper = OrganizationMapper

    def _with_related(self):
        query = select(self.model) \
            .options(
                selectinload(self.model.phones),
                selectinload(self.model.building),
                selectinload(self.model.organization_activities)
                .selectinload(OrganizationActivity.activity)
            )
        return query

    async def get_all(self) -> List[OrganizationRead]:
        query = self._with_related()
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(org) for org in res.scalars().all()]


    async def get_one(self, id: int) -> OrganizationRead:
        query = self._with_related().filter(self.model.id == id)
        res = await self.session.execute(query)
        obj = res.scalar_one_or_none()
        if obj is None:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} with id={id} not found")
        return self.mapper.map_to_domain_entity(obj)


    async def get_filtered(self, **filter_by) -> List[OrganizationRead]:
        query = self._with_related().filter_by(**filter_by)
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(org) for org in res.scalars().all()]


    async def get_by_activity_ids(self, activity_ids: List[int]) -> List[OrganizationRead]: 
        query = self._with_related() \
            .join(OrganizationActivity, OrganizationActivity.organization_id == self.model.id) \
            .filter(OrganizationActivity.activity_id.in_(activity_ids)) \
            .distinct()

        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in res.scalars().all()]

    async def search_by_name(self, query: str) -> List[OrganizationRead]:
        query = self._with_related().filter(self.model.name.contains(query.strip().lower()))
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in res.scalars().all()]

    async def remove_phones(self, organization_id: int):
        stmt = delete(Phone).where(Phone.organization_id == organization_id)
        await self.session.execute(stmt)

    async def remove_activity_links(self, organization_id: int):
        stmt = delete(OrganizationActivity).where(OrganizationActivity.organization_id == organization_id)
        await self.session.execute(stmt)

    async def add_phones(self, organization_id: int, phone_numbers: List[str]):
        phones = [Phone(number=number, organization_id=organization_id) for number in phone_numbers]
        if phones:
            self.session.add_all(phones)

    async def add_activity_rel(self, organization_id: int, activity_ids: List[int]):
        links = [
            OrganizationActivity(organization_id=organization_id, activity_id=activity_id)
            for activity_id in activity_ids
        ]
        if links:
            self.session.add_all(links)