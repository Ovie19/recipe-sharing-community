from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlmodel import Session
from app.config.dependencies import get_session
from app.models.review import ReviewResponse, ReviewCreate, ReviewUpdateResponse, ReviewUpdateRequest
from app.repositories import UserRepository
from app.repositories.recipe_repository import RecipeRepository
from app.repositories.review_repository import ReviewRepository
from app.services.review_service import ReviewService

router = APIRouter(prefix="/review", tags=["Reviews"])

def get_review_repo(session:Session = Depends(get_session))->ReviewRepository:
    repository = ReviewRepository(session)
    return repository
def get_recipe_repo(session:Session = Depends(get_session))->RecipeRepository:
    repository = RecipeRepository(session)
    return repository
def get_user_repo(session:Session = Depends(get_session))->UserRepository:
    repository = UserRepository(session)
    return repository

def get_review_service(review_repo:ReviewRepository = Depends(get_review_repo),
                       user_repo:UserRepository = Depends(get_user_repo),
                       recipe_repo:RecipeRepository = Depends(get_recipe_repo))->ReviewService:
    review_service = ReviewService(review_repo,user_repo,recipe_repo)
    return review_service

@router.post("/create", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(payload: ReviewCreate, review_service: ReviewService = Depends(get_review_service)):
    return review_service.create_review(payload)

@router.patch("/update/{review_id}", response_model=ReviewUpdateResponse, status_code=status.HTTP_200_OK)
def update_review(review_id: UUID, payload: ReviewUpdateRequest,review_service: ReviewService = Depends(get_review_service))->ReviewUpdateResponse:
    return review_service.update_review(review_id,payload)
