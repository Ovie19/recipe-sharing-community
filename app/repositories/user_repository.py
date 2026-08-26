from typing import Optional
from uuid import UUID

from sqlmodel import Session
from app.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def find_by_id(self, user_id: UUID) -> type[User] | None:
        return self.session.get(User, user_id)