from typing import List

from src.schemas import OrganizationRead, OrganizationCreate, ActivityRead, OrganizationBase
from src.services.base import BaseService
from src.repositories.organization import OrganizationRepository 
from src.services.activity import ActivityService
from src.models import Phone, OrganizationActivity

from sqlalchemy import delete


class OrganizationService(BaseService):
    def __init__(self, db):
        super().__init__(db)
        self.repo = OrganizationRepository(self.db.session)

    async def get_all(self) -> List[OrganizationRead]:
        return await self.repo.get_all()

    async def get_by_id(self, id: int) -> OrganizationRead:
        return await self.repo.get_one(id=id)

    async def get_by_building(self, building_id: int) -> List[OrganizationRead]:
        return await self.repo.get_filtered(building_id=building_id)

    async def get_by_activity_ids(self, activity_ids: List[int]) -> List[OrganizationRead]:
        return await self.repo.get_by_activity_ids(activity_ids)

    async def search_by_name(self, query: str) -> List[OrganizationRead]:
        return await self.repo.search_by_name(query)
    
    async def get_by_activity_with_children(self, activity_id: int, max_depth: int = 3) -> List[OrganizationRead]:
        activity_service = ActivityService(self.db)
        tree = await activity_service.get_tree_by_id(activity_id, max_depth=max_depth)

        def collect_ids(node: ActivityRead) -> List[int]:
            ids = [node.id]
            for child in node.children:
                ids.extend(collect_ids(child))
            return ids
        
        activity_ids = collect_ids(tree)
        return await self.get_by_activity_ids(activity_ids)

    async def create(self, data: OrganizationCreate) -> OrganizationRead:
        organization = await self.repo.add(data)

        await self.repo.add_phones(organization.id, data.phone_numbers)
        await self.repo.add_activity_rel(organization.id, data.activity_ids)

        await self.db.commit()
        return await self.get_by_id(organization.id)

    async def update(self, id: int, data: OrganizationCreate) -> OrganizationRead:
        await self.repo.edit(data=data, id=id)

        await self.repo.remove_phones(id)
        await self.repo.remove_activity_links(id)

        await self.repo.add_phones(id, data.phone_numbers)
        await self.repo.add_activity_rel(id, data.activity_ids)

        await self.db.commit()
        return await self.get_by_id(id)

    async def delete(self, id: int) -> None:
        await self.repo.delete(id=id)
        await self.db.commit()