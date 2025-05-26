from fastapi import APIRouter, Depends, Query, status
from typing import List

from src.api.dependencies import get_db_manager, check_api_key
from src.schemas import OrganizationRead, OrganizationCreate
from src.services.organization import OrganizationService
from src.db_manager import DBManager
from src.api.dependencies import APIKEYDep, DBDep

router = APIRouter(prefix="/organizations", tags=["organizations"], dependencies=[APIKEYDep])


@router.get("/", response_model=List[OrganizationRead])
async def get_all(db: DBManager = DBDep):
    return await OrganizationService(db).get_all()

@router.get("/search", response_model=List[OrganizationRead])
async def search_by_name(query: str = Query(..., min_length=2), db: DBManager = DBDep):
    return await OrganizationService(db).search_by_name(query)

@router.get("/{id}", response_model=OrganizationRead)
async def get_by_id(id: int, db: DBManager = DBDep):
    return await OrganizationService(db).get_by_id(id)


@router.get("/by-building/{building_id}", response_model=List[OrganizationRead])
async def get_by_building(building_id: int, db: DBManager = DBDep):
    return await OrganizationService(db).get_by_building(building_id)


@router.get("/by-activity/{activity_id}", response_model=List[OrganizationRead])
async def get_by_activity(activity_id: int, db: DBManager = DBDep):
    return await OrganizationService(db).get_by_activity_ids([activity_id])


@router.get("/by-activity-tree/{activity_id}", response_model=List[OrganizationRead])
async def get_by_activity_tree(activity_id: int, db: DBManager = DBDep):
    return await OrganizationService(db).get_by_activity_with_children(activity_id)


@router.post("/", response_model=OrganizationRead, status_code=201)
async def create_organization(data: OrganizationCreate, db: DBManager = DBDep):
    return await OrganizationService(db).create(data)

@router.put("/{id}", response_model=OrganizationRead)
async def update_organization(id: int, data: OrganizationCreate, db: DBManager = DBDep):
    return await OrganizationService(db).update(id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(id: int, db: DBManager = DBDep):
    await OrganizationService(db).delete(id)
