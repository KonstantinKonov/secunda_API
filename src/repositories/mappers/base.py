from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel
from sqlalchemy import Row, RowMapping

from src.database import Base


DTOModel = TypeVar("DTOModel", bound=BaseModel)
ORMModel = TypeVar("ORMModel", bound=Base)


class DataMapper(ABC, Generic[ORMModel, DTOModel]):

    @classmethod
    @abstractmethod
    def map_to_domain_entity(cls, model: ORMModel) -> DTOModel:
        pass

    @classmethod
    @abstractmethod
    def map_to_orm_entity(cls, dto: DTOModel) -> ORMModel:
        pass