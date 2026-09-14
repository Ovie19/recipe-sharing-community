from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.models.user import UserResponse
from app.repositories import UserRepository
from app.services.authentication import AuthenticationService
from app.models.auth import LoginRequest
from app.models.user import UserCreate
from app.security import PasswordHasher
from app.config.dependencies import get_session

router = APIRouter(prefix="/authentication", tags=["Authentication"])
password_hash = PasswordHasher()

def get_auth_service(session:Session = Depends(get_session))->AuthenticationService:
    repository = UserRepository(session)
    authentication_service = AuthenticationService(repository,password_hash)
    return authentication_service

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, auth_service: AuthenticationService = Depends(get_auth_service)):
    return auth_service.create_user(payload)

@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login_user(payload: LoginRequest,auth_service: AuthenticationService = Depends(get_auth_service)):
    return auth_service.login_user(payload)

