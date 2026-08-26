from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session

from app.models.recipe import RecipeCreate, RecipeResponse, Recipe
from app.repositories.recipe_repository import RecipeRepository

class RecipeService:
    def __init__(self, session: Session):
        self.repository = RecipeRepository(session)

    def create_recipe(self, recipe_in: RecipeCreate, user_id: UUID) -> RecipeResponse:
        recipe = Recipe.model_validate(recipe_in, update={"user_id": user_id})
        created_recipe = self.repository.create(recipe)
        return RecipeResponse.model_validate(created_recipe)

    def get_recipe(self, recipe_id: UUID) -> Optional[RecipeResponse]:
        recipe = self.repository.get_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return RecipeResponse.model_validate(recipe)

    def view_recipes(self, skip: int = 0, limit: int = 100) -> List[RecipeResponse]:
        recipes = self.repository.get_all(skip=skip, limit=limit)
        return [RecipeResponse.model_validate(recipe) for recipe in recipes]

    def update_recipe(self, recipe_id: UUID, recipe_in: RecipeCreate) -> RecipeResponse:
        update_data = recipe_in.model_dump(exclude_unset=True)
        updated_recipe = self.repository.update(recipe_id, update_data)
        if not updated_recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return RecipeResponse.model_validate(updated_recipe)

    def delete_recipe(self, recipe_id: UUID) -> bool:
        success = self.repository.delete(recipe_id)
        if not success:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return True
