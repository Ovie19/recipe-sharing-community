from uuid import uuid4
from unittest.mock import Mock

import pytest

from app.exception import AuthenticationException
from app.repositories import UserRepository
from app.services import AuthenticationService
from app.models import User, UserCreate, UserResponse
from app.security import PasswordHasher


class TestAuthenticationService:
    @pytest.fixture
    def repository(self):
        return Mock(spec=UserRepository)

    @pytest.fixture
    def password_hasher(self):
        return Mock(spec=PasswordHasher)

    @pytest.fixture
    def service(self, repository, password_hasher):
        return AuthenticationService(repository, password_hasher)

    def test_create_user(self, repository, password_hasher, service):
        user_id = uuid4()

        user_request = UserCreate(
            username="test-username",
            email="email@test-email.com",
            password="test-password"
        )

        hashed_password = "hashed-password"
        password_hasher.hash.return_value = hashed_password

        repository.exists_by_email.return_value = False
        repository.exists_by_username.return_value = False

        repository.save.return_value = User(
            id=user_id,
            username="test-username",
            email="email@test-email.com",
            password=hashed_password
        )

        result = service.create_user(user_request)

        assert result == UserResponse(
            id=user_id,
            username="test-username",
            email="email@test-email.com",
        )

        repository.save.assert_called_once()
        password_hasher.hash.assert_called_once_with("test-password")

        saved_user = repository.save.call_args.args[0]
        assert saved_user.username == user_request.username
        assert saved_user.email == user_request.email
        assert saved_user.password != user_request.password
        assert saved_user.password == hashed_password

    def test_create_new_user_with_existing_email(self, repository, service):
        user_request = UserCreate(
            username="test-username",
            email="email@test-email.com",
            password="test-password"
        )

        repository.exists_by_email.return_value = True
        with pytest.raises(AuthenticationException):
            service.create_user(user_request)

    def test_create_new_user_with_existing_username(self, repository, service):
        user_request = UserCreate(
            username="test-username",
            email="email@test-email.com",
            password="test-password"
        )

        repository.exists_by_email.return_value = False
        repository.exists_by_username.return_value = True
        with pytest.raises(AuthenticationException):
            service.create_user(user_request)