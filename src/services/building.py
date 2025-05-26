from typing import List

from src.schemas import BuildingRead, BuildingCreate
from src.services.base import BaseService
from src.repositories.building import BuildingRepository


class BuildingService(BaseService):
    def __init__(self, db):
        super().__init__(db)
        self.repo = BuildingRepository(self.db.session)

    async def get_all(self) -> List[BuildingRead]:
        return await self.repo.get_all()

    async def get_by_id(self, id: int) -> BuildingRead:
        return await self.repo.get_one(id=id)

    async def create(self, data: BuildingCreate) -> BuildingRead:
        building = await self.repo.add(data)
        await self.db.commit()
        return building

    async def update(self, id: int, data: BuildingCreate) -> BuildingRead:
        await self.repo.edit(data=data, id=id)
        await self.db.commit()
        return await self.get_by_id(id)

    async def delete(self, id: int) -> None:
        await self.repo.delete(id=id)
        await self.db.commit()
    