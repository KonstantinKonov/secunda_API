import logging
from typing import Sequence, Any, List

from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.repositories.mappers.base import DataMapper

class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> list[BaseModel | Any]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs) -> list[BaseModel | Any]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) -> BaseModel | None | Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="not found")
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> BaseModel | Any:
        try:
            raw_data = data.model_dump()
            filtered_columns = {col.name for col in self.model.__table__.columns}
            filtered_data = {k: v for k, v in raw_data.items() if k in filtered_columns}

            add_data_stmt = insert(self.model).values(**filtered_data).returning(self.model)
            res = await self.session.execute(add_data_stmt)
            #model = result.scalars().one()
            #return self.mapper.map_to_domain_entity(model)
            return res.scalars().one()
        except IntegrityError as ex:
            logging.exception(
                f"Не удалось добавить данные в БД, входные данные={data}"
            )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise HTTPException from ex
            else:
                logging.exception(
                    f"Незнакомая ошибка: не удалось добавить данные в БД, входные данные={data}"
                )
                raise ex

    async def add_bulk(self, data: Sequence[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, id: int, data: BaseModel) -> None:
        raw_data = data.model_dump(exclude_unset=True)

        valid_columns = {col.name for col in self.model.__table__.columns}
        filtered_data = {k: v for k, v in raw_data.items() if k in valid_columns}

        update_stmt = update(self.model) \
            .where(self.model.id==id) \
            .values(**filtered_data)

        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
