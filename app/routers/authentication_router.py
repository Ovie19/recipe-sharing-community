from fastapi import APIRouter
from services.authentication import AuthenticationService
from app.models.user import UserCreate, LoginRequest

router = APIRouter()

authentication_service = AuthenticationService()

@router.post("/register")
def create_user(payload: UserCreate):
    return authentication_service.create_user(payload)

@router.post("/login")
def login_user(payload: LoginRequest):
    return authentication_service.login_user(payload)

