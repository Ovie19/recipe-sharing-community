from datetime import datetime,timezone
from uuid import UUID, uuid4


from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    user_id: UUID
    recipe_id: UUID
    comment: str

class ReviewResponse(BaseModel):
    id: UUID
    user_id: UUID
    recipe_id: UUID
    comment: str

class ReviewUpdateRequest(BaseModel):
    comment: str

class ReviewUpdateResponse(BaseModel):
    id: UUID
    comment: str

class DeleteReviewRequest(BaseModel):
    user_id: UUID


class DeleteReviewResponse(BaseModel):
    status: str

class Review(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    comment: str
    user_id: UUID
    recipe_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))