import pytest
from pydantic import ValidationError

from app.models import UserCreate

class TestUser:
    @pytest.mark.parametrize("email", [
        "ade@aaa",
        "invalid-email",
        "@gmail.com",
        "short@.com"
    ])
    def test_user_create_with_invalid_email(self, email):
        with pytest.raises(ValidationError):
            UserCreate(
                username="john",
                email=email,
                password="valid-password",
            )

    @pytest.mark.parametrize("email", [
        "ade@aaa.com",
        "ade@gmail.com",
        "ade@yahoo.com"
    ])
    def test_user_create_with_valid_email(self, email):
        user = UserCreate(
            username="john",
            email=email,
            password="password123"
        )

        assert user.username == "john"
        assert user.email == email
        assert user.password == "password123"

    @pytest.mark.parametrize("password", [
        "1234",
        "12345",
        "gffafaf",
        "haahah",
        "123456789abcdefghijkl"
    ])
    def test_user_create_with_invalid_password(self, password):
        with pytest.raises(ValidationError):
            UserCreate(
                username="john",
                email="john@gmail.com",
                password=password
            )

    @pytest.mark.parametrize("password", [
        "a1e@a56com",
        "4563das$%com",
        "ads467ks822dhwva@#$%"
    ])
    def test_user_create_with_valid_password(self, password):
        user = UserCreate(
            username="john",
            email="john@gmail.com",
            password=password
        )

        assert user.username == "john"
        assert user.email == "john@gmail.com"
        assert user.password == password