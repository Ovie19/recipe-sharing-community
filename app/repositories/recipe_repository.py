from typing import List, Optional, cast
from unittest import result
from uuid import UUID
from sqlmodel import Session, select, func
from app.models.recipe import Recipe

class RecipeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, recipe: Recipe) -> Recipe:
        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)
        return recipe

    def get_recipe_by_id(self,recipe_id: UUID) -> Optional[Recipe]:
        return self.session.get(Recipe,recipe_id)

    def view_all_recipes(self,skip: int = 0,limit: int = 100) -> List[Recipe]:
        statement = (select(Recipe).offset(skip).limit(limit))
        results = self.session.exec(statement).all()
        return list(results)

    def update_recipe(self,recipe_id: UUID,recipe_data: dict) -> Optional[Recipe]:
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return None
        for key, value in recipe_data.items():
            setattr(recipe, key, value)
        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)
        return recipe

    def delete(self, recipe_id: UUID) -> bool:
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return False
        self.session.delete(recipe)
        self.session.commit()
        return True

    def count(self) -> int:
        statement = select(func.count(Recipe.id))
        result = self.session.exec(statement).one()
        return cast(int,result)
