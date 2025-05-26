from fastapi import APIRouter

from src.api.organization import router as organization_router
from src.api.activity import router as activity_router
from src.api.building import router as building_router

api_router = APIRouter()

api_router.include_router(organization_router)
api_router.include_router(activity_router)
api_router.include_router(building_router)
