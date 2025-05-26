from fastapi import APIRouter, Depends, Query, status
from typing import List

from src.api.dependencies import DBDep, APIKEYDep
from src.services.activity import ActivityService
from src.schemas import ActivityRead, ActivityCreate
from src.db_manager import DBManager

router = APIRouter(prefix="/activities", tags=["activities"], dependencies=[APIKEYDep])


@router.get("/", response_model=List[ActivityRead])
async def get_all_activities(db: DBManager = DBDep):
    return await ActivityService(db).get_all()


@router.get("/{id}", response_model=ActivityRead)
async def get_activity_by_id(id: int, db: DBManager = DBDep):
    return await ActivityService(db).get_one_by_id(id)


@router.get("/tree/{id}", response_model=ActivityRead)
async def get_activity_tree(id: int, db: DBManager = DBDep, max_depth: int = Query(3, ge=1)):
    return await ActivityService(db).get_tree_by_id(id=id, max_depth=max_depth)


@router.post("/", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
async def create_activity(data: ActivityCreate, db: DBManager = DBDep):
    return await ActivityService(db).create(data)

@router.put("/{id}", response_model=ActivityRead)
async def update_activity(id: int, data: ActivityCreate, db: DBManager = DBDep):
    return await ActivityService(db).update(id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(id: int, db: DBManager = DBDep):
    await ActivityService(db).delete(id)