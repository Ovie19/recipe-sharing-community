from app.exception import AuthenticationException
from app.repositories import UserRepository
from app.models import UserCreate, UserResponse, User
from app.security import PasswordHasher

class AuthenticationService:
    def __init__(
            self,
            repository: UserRepository,
            password_hasher: PasswordHasher
    ):
        self.repository = repository
        self.password_hasher = password_hasher

    def create_user(self, payload: UserCreate) -> UserResponse:
        if self.repository.exists_by_email(payload.email):
            raise AuthenticationException("User with this email already exists")

        if self.repository.exists_by_username(payload.username):
            raise AuthenticationException("User with this username already exists")

        data = payload.model_dump()
        user = User(**data)
        user.password = self.password_hasher.hash(user.password)
        user = self.repository.save(user)
        return UserResponse.model_validate(user)
