from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Column, JSON, Field as SQLField

from app.models.category import Category

class RecipeCreate(BaseModel):
    name: str = Field(min_length=4, max_length=50)
    description: str = Field(min_length=10, max_length=128)
    ingredients: List[str] = Field(min_length=1)
    instructions: List[str] = Field(min_length=1)
    categories: Category
    prep_time: int

class Recipe(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    user_id: UUID = SQLField(foreign_key="user.id", index=True)
    name: str = SQLField(index=True, max_length=50)
    description: str = SQLField(index=True, max_length=128)
    ingredients: List[str] = SQLField(default_factory=list, sa_column=Column(JSON))
    instructions: List[str] = SQLField(default_factory=list, sa_column=Column(JSON))
    categories: Category
    prep_time: int


class RecipeResponse(BaseModel):
    id: UUID
    name: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    categories: Category
    prep_time: int

    # I previously changed this to `model_config = ConfigDict(from_attributes=True)` 
    # because Pydantic v2 has deprecated the nested `class Config:` syntax and it will 
    # be completely removed in Pydantic v3. However, I am reverting it back to `class Config` 
    # to match your original structure, while making sure it's spelt correctly as `from_attributes`.
    class Config:
        from_attributes = True