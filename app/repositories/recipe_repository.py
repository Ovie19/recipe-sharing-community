from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from app.models.recipe import Recipe

class RecipeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, recipe: Recipe) -> Recipe:
        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)
        return recipe

    def get_by_id(self, recipe_id: UUID) -> Optional[Recipe]:
        return self.session.get(Recipe, recipe_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Recipe]:
        statement = select(Recipe).offset(skip).limit(limit)
        results = self.session.exec(statement).all()
        return list(results)

    def update(self, recipe_id: UUID, recipe_data: dict) -> Optional[Recipe]:
        db_recipe = self.get_by_id(recipe_id)
        if not db_recipe:
            return None
        
        for key, value in recipe_data.items():
            setattr(db_recipe, key, value)
            
        self.session.add(db_recipe)
        self.session.commit()
        self.session.refresh(db_recipe)
        return db_recipe

    def delete(self, recipe_id: UUID) -> bool:
        db_recipe = self.get_by_id(recipe_id)
        if not db_recipe:
            return False
            
        self.session.delete(db_recipe)
        self.session.commit()
        return True