from uuid import uuid4

import pytest
from sqlmodel import SQLModel, create_engine, Session

from app.models import User
from app.repositories import UserRepository

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

class TestUserRepository:
    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(test_engine)
        with Session(test_engine) as session:
            yield session
        SQLModel.metadata.drop_all(test_engine)

    def test_save(self, session):
        repo = UserRepository(session)

        user = User(
            username="john",
            email="john@gmail.com",
            password="hagsjassgs"
        )

        saved_user = repo.save(user)
        assert saved_user.id is not None
        assert saved_user.username == "john"

    def test_find_by_id(self, session):
        repo = UserRepository(session)

        user = User(
            username="john",
            email="john@gmail.com",
            password="hagsjassgs"
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        found_user = repo.find_by_id(user.id)
        assert found_user is not None
        assert found_user.username == "john"
        assert found_user.email == "john@gmail.com"

    def test_find_by_id_returns_none_when_user_does_not_exist(self, session):
        repo = UserRepository(session)
        found_user = repo.find_by_id(uuid4())
        assert found_user is None