from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.api.router import api_router
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    logging.info("FastAPI initialized")
    yield
    # При выключении/перезагрузке приложения


app = FastAPI(lifespan=lifespan, title="secunda API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(api_router)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck():
    return {"healthcheck": "OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
