from fastapi import FastAPI
from app.routers.authentication_router import router as authentication_router
from contextlib import asynccontextmanager

from app.config.database import create_db_and_tables
import app.models

@asynccontextmanager
async def lifespan(recipe_app: FastAPI):
    create_db_and_tables()
    yield

recipe_app = FastAPI(lifespan=lifespan)

recipe_app.include_router(authentication_router)