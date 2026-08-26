from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import recipe
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(recipe.router)