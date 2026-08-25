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

    @pytest.fixture
    def saved_user(self, session) -> User:
        user = User(
            username="john",
            email="john@gmail.com",
            password="test-password",
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def test_save(self, session):
        repo = UserRepository(session)

        user = User(
            username="john",
            email="john@gmail.com",
            password="test-password"
        )

        saved_user = repo.save(user)
        assert saved_user.id is not None
        assert saved_user.username == "john"

    def test_find_by_id(self, session, saved_user):
        repo = UserRepository(session)

        found_user = repo.find_by_id(saved_user.id)
        assert found_user is not None
        assert found_user.username == "john"
        assert found_user.email == "john@gmail.com"

    def test_find_by_id_returns_none_when_user_does_not_exist(self, session):
        repo = UserRepository(session)
        found_user = repo.find_by_id(uuid4())
        assert found_user is None

    def test_find_by_email(self, session, saved_user):
        repo = UserRepository(session)

        found_user = repo.find_by_email(saved_user.email)
        assert found_user is not None
        assert found_user.username == "john"
        assert found_user.email == "john@gmail.com"

    def test_find_by_email_returns_none_when_user_does_not_exist(self, session):
        repo = UserRepository(session)
        found_user = repo.find_by_email("fake@gmail.com")
        assert found_user is None

    def test_exist_by_email(self, session, saved_user):
        repo = UserRepository(session)
        assert repo.exists_by_email(saved_user.email)

    def test_exist_by_email_returns_false_when_user_does_not_exist(self, session):
        repo = UserRepository(session)
        assert not repo.exists_by_email("fake@gmail.com")

    def test_find_by_username(self, session, saved_user):
        repo = UserRepository(session)

        found_user = repo.find_by_username(saved_user.username)
        assert found_user is not None
        assert found_user.username == "john"
        assert found_user.email == "john@gmail.com"

    def test_find_by_username_returns_none_when_user_does_not_exist(self, session):
        repo = UserRepository(session)
        found_user = repo.find_by_username("john_constantine")
        assert found_user is None

    def test_exist_by_username(self, session, saved_user):
        repo = UserRepository(session)
        assert repo.exists_by_username(saved_user.username)

    def test_exist_by_username_returns_false_when_user_does_not_exist(self, session):
        repo = UserRepository(session)
        assert not repo.exists_by_username("john_constantine")