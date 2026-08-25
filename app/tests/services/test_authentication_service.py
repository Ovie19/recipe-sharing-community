from uuid import uuid4
from unittest.mock import Mock

import pytest

from app.exception import AuthenticationException
from app.repositories import UserRepository
from app.services import AuthenticationService
from app.models import User, UserCreate, UserResponse, LoginRequest
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

    def test_login_user_with_invalid_username(self, repository, service):
        login_request = LoginRequest(username="test-username", password="test-password")
        repository.find_by_username.return_value = None
        with pytest.raises(AuthenticationException):
            service.login_user(login_request)

    def test_login_user_password_does_not_match(self, repository, password_hasher, service):
        login_request = LoginRequest(username="test-username", password="fake-password")
        repository.find_by_username.return_value = User(
            id=uuid4(),
            username="test-username",
            email="email@test-email.com",
            password="hashed_password"
        )
        password_hasher.verify.return_value = False
        with pytest.raises(AuthenticationException):
            service.login_user(login_request)

    def test_login_user_successful(self, repository, password_hasher, service):
        user_id = uuid4()
        login_request = LoginRequest(username="test-username", password="test-password")
        repository.find_by_username.return_value = User(
            id=user_id,
            username="test-username",
            email="email@test-email.com",
            password="hashed_password"
        )
        password_hasher.verify.return_value = True

        result = service.login_user(login_request)

        assert result is not None
        assert result.id == user_id
        assert result.username == "test-username"
        assert result.email == "email@test-email.com"