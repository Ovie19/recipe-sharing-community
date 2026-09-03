from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Column, JSON, Field as SQLField

from .category import Category

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

    class Config:
        from_attributes = True