from datetime import date
from typing import List, Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import Activity
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ActivityMapper
from src.schemas import ActivityCreate, ActivityRead


class ActivityRepository(BaseRepository):
    model = Activity
    mapper = ActivityMapper


    def build_activity_tree(self, activity: Activity, max_depth: int = 3) -> ActivityRead:
        def inner_build(node: Activity, depth: int) -> ActivityRead:
            try:
                children = node.children if depth < max_depth else []
            except Exception:
                children = []

            return ActivityRead(
                id=node.id,
                name=node.name,
                parent_id=node.parent_id,
                children=[inner_build(child, depth + 1) for child in children]
            )

        return inner_build(activity, 1)


    async def get_all(self) -> List[ActivityRead]:
        stmt = select(self.model).options(selectinload(self.model.children))
        res = await self.session.execute(stmt)
        return [self.mapper.map_to_domain_entity(obj) for obj in res.scalars().all()]

    async def get_filtered(self, **filter_by) -> List[ActivityRead]:
        query = select(self.model) \
            .filter_by(**filter_by) \
            .options(selectinload(self.model.children))

        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(obj) for obj in res.scalars().all()]


    async def get_tree_by_id(self, id: int, max_depth:int = 3) -> ActivityRead:
        query = select(self.model) \
            .filter_by(id=id) \
            .options(selectinload(self.model.children))
        res = await self.session.execute(query)
        activity = res.scalar_one_or_none()

        if activity is None:
            raise HTTPException(status_code=404)

        return self.build_activity_tree(activity, max_depth=max_depth)


    async def get_one(self, id: int) -> ActivityRead:
        query = select(self.model) \
            .filter_by(id=id) \

        res = await self.session.execute(query)
        obj = res.scalar_one_or_none()
        if obj is None:
            raise HTTPException(f"{self.model.__name__} with id={id} not found")
        return self.mapper.map_to_domain_entity(obj)

    async def get_one_or_none(self, **filter_by) -> ActivityRead | None:
        query = select(self.model) \
            .filter_by(**filter_by) \
            .options(selectinload(self.model.children))

        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_children_by_parents(self, parent_ids: List[int]) -> List[ActivityRead]:
        return await self.get_filtered(parent_id=parent_ids)