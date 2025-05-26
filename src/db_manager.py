from src.repositories.organization import OrganizationRepository
from src.repositories.building import BuildingRepository 
from src.repositories.activity import ActivityRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.organization = OrganizationRepository(self.session)
        self.building = BuildingRepository(self.session)
        self.activity = ActivityRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
