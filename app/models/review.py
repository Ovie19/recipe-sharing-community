from datetime import datetime,timezone
from uuid import UUID, uuid4


from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField


class ReviewCreate(BaseModel):
    user_id: UUID
    recipe_id: UUID
    comment: str = Field(min_length=3, max_length=500)

class ReviewResponse(BaseModel):
    id: UUID
    user_id: UUID
    recipe_id: UUID
    comment: str

class ReviewUpdateRequest(BaseModel):
    comment: str = Field(min_length=3, max_length=500)

class ReviewUpdateResponse(BaseModel):
    id: UUID
    comment: str

class DeleteReviewRequest(BaseModel):
    user_id: UUID


class DeleteReviewResponse(BaseModel):
    status: str

class Review(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    comment: str = SQLField(index=True, max_length=500)
    user_id: UUID = SQLField(foreign_key="user.id", index=True)
    recipe_id: UUID = SQLField(foreign_key="recipe.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))