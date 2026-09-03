from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Depends
from sqlmodel import Session

from app.config.dependencies import get_session
from app.models.recipe import RecipeCreate, RecipeResponse
from app.services.recipe_service import RecipeService


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)


def get_recipe_service(
    session: Session = Depends(get_session)) -> RecipeService:
    return RecipeService(session)


@router.post(
    "/",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED)
def create_recipe(recipe_in: RecipeCreate,user_id: UUID,service: RecipeService = Depends(get_recipe_service)):
    return service.create_recipe(recipe_in, user_id)


@router.get(
    "/",
    response_model=List[RecipeResponse]
)
def get_recipes(
    skip: int = 0,
    limit: int = 100,
    service: RecipeService = Depends(get_recipe_service)
):
    return service.view_recipes(skip=skip, limit=limit)


@router.get(
    "/{recipe_id}",
    response_model=RecipeResponse
)
def get_recipe(
    recipe_id: UUID,
    service: RecipeService = Depends(get_recipe_service)
):
    return service.get_recipe(recipe_id)


@router.put(
    "/{recipe_id}",
    response_model=RecipeResponse
)
def update_recipe(
    recipe_id: UUID,
    recipe_in: RecipeCreate,
    service: RecipeService = Depends(get_recipe_service)
):
    return service.update_recipe(recipe_id, recipe_in)


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_recipe(
    recipe_id: UUID,
    service: RecipeService = Depends(get_recipe_service)
):
    service.delete_recipe(recipe_id)
    return None