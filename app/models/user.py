from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr
from sqlmodel import SQLModel, Field as SQLField

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)

class User(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    username: str = SQLField(unique=True, index=True, max_length=20)
    email: EmailStr = SQLField(unique=True, index=True)
    password: str

from pydantic import ConfigDict

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)