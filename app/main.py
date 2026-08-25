from fastapi import FastAPI
from app.config.database import create_db_and_tables
from app.models.user import User
from app.models.recipe import Recipe
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)