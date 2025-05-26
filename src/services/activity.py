from typing import List, Any

from src.schemas import ActivityRead, ActivityCreate
from src.services.base import BaseService
from src.repositories.activity import ActivityRepository

from sqlalchemy import select
from sqlalchemy.orm import selectinload

class ActivityService(BaseService):
    def __init__(self, db):
        super().__init__(db)
        self.repo = ActivityRepository(self.db.session)


    async def get_all(self) -> List[ActivityRead]:
        return await self.repo.get_all()


    async def get_one_by_id(self, id: int) -> ActivityRead:
        return await self.repo.get_tree_by_id(id=id, max_depth=1)


    async def get_tree_by_id(self, id: int, max_depth: int = 0) -> ActivityRead:
        return await self.repo.get_tree_by_id(id=id, max_depth=max_depth)


    async def create(self, data: ActivityCreate) -> ActivityRead:
        activity = await self.repo.add(data)
        await self.db.commit()
        return activity


    async def update(self, id: int, data: ActivityCreate) -> ActivityRead:
        await self.repo.edit(data=data, id=id)
        await self.db.commit()
        return await self.get_one_by_id(id)


    async def delete(self, id: int) -> None:
        await self.repo.delete(id=id)
        await self.db.commit()