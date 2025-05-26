from fastapi import APIRouter, Depends, status
from typing import List

from src.api.dependencies import DBDep, APIKEYDep
from src.services.building import BuildingService 
from src.schemas import BuildingRead, BuildingCreate
from src.db_manager import DBManager

router = APIRouter(prefix="/buildings", tags=["buildings"], dependencies=[APIKEYDep])


@router.get("/", response_model=List[BuildingRead])
async def get_all_buildings(db: DBManager = DBDep):
    return await BuildingService(db).get_all()


@router.get("/{id}", response_model=BuildingRead)
async def get_building_by_id(id: int, db: DBManager = DBDep):
    return await BuildingService(db).get_by_id(id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_building(data: BuildingCreate, db: DBManager = DBDep):
    return await BuildingService(db).create(data)

@router.put("/{id}", response_model=BuildingRead)
async def update_building(id: int, data: BuildingCreate, db: DBManager = DBDep):
    return await BuildingService(db).update(id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(id: int,  db: DBManager = DBDep):
    await BuildingService(db).delete(id)