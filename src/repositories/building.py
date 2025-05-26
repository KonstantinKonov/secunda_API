from fastapi import HTTPException
from sqlalchemy import select

from src.models import Building
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BuildingMapper
from src.schemas.building import BuildingCreate


class BuildingRepository(BaseRepository):
    model = Building
    mapper = BuildingMapper
