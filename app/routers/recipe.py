from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.dependencies import get_session
from app.models.recipe import RecipeCreate, RecipeResponse
from app.services.recipe_services import RecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])

def get_recipe_service(session: Session = Depends(get_session)) -> RecipeService:
    return RecipeService(session)

@router.post("/", response_model=RecipeResponse)
def create_recipe(
    recipe_in: RecipeCreate,
    service: RecipeService = Depends(get_recipe_service)
):
    # For now, we mock a user_id since we don't have auth middleware yet
    mock_user_id = uuid4()
    return service.create_recipe(recipe_in, mock_user_id)

@router.get("/", response_model=List[RecipeResponse])
def get_recipes(
    skip: int = 0,
    limit: int = 100,
    service: RecipeService = Depends(get_recipe_service)
):
    return service.get_recipes(skip=skip, limit=limit)

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: UUID,
    service: RecipeService = Depends(get_recipe_service)
):
    return service.get_recipe(recipe_id)

@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: UUID,
    recipe_in: RecipeCreate,
    service: RecipeService = Depends(get_recipe_service)
):
    return service.update_recipe(recipe_id, recipe_in)

@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(
    recipe_id: UUID,
    service: RecipeService = Depends(get_recipe_service)
):
    service.delete_recipe(recipe_id)
