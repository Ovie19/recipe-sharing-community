import uuid
from typing import List

from app.models.review import ReviewResponse, Review, ReviewUpdateResponse, DeleteReviewRequest, \
    DeleteReviewResponse, ReviewUpdateRequest
from app.models.review import ReviewCreate
from app.repositories.review_repository import ReviewRepository
from app.repositories.user import UserRepository
from app.repositories.recipe_repository import RecipeRepository


class ReviewService:
    def __init__(self, review_repository: ReviewRepository, user_repository: UserRepository, recipe_repository: RecipeRepository):
        self.review_repository = review_repository
        self.user_repo = user_repository
        self.recipe_repo = recipe_repository

    review_id = uuid.UUID("7f3c2a91-6e54-4b87-a1d9-3c8e5f204b76")

    def create_review(self, request:ReviewCreate)->ReviewResponse:
        found_user = self.user_repo.find_by_id(request.user_id)
        if found_user is None:
            raise ValueError("User does not exist")
        found_recipe = self.recipe_repo.get_recipe_by_id(request.recipe_id)
        if found_recipe is None:
            raise ValueError("Recipe does not exist")

        review = Review(id=self.review_id,
                        comment=request.comment,
                        user_id=request.user_id,
                        recipe_id=request.recipe_id)
        saved_review = self.review_repository.save(review)
        review_response = ReviewResponse(id=saved_review.id,
                                         user_id=saved_review.user_id,
                                         recipe_id=saved_review.recipe_id,
                                         comment=saved_review.comment,)
        return review_response

    def update_review(self, review_id, update_request:ReviewUpdateRequest)->ReviewUpdateResponse:
        found_review = self.review_repository.find_by_id(review_id)
        if found_review is None:
            raise ValueError(f"Review id {review_id} not found")
        update_data = update_request.model_dump(exclude_unset=True)
        update = self.review_repository.update(review_id, update_data)
        if update is None:
            raise ValueError("failed to update")
        update_response = ReviewUpdateResponse(id=update.recipe_id,comment=update.comment)
        return update_response

    def delete_review(self,review_id,request:DeleteReviewRequest)->DeleteReviewResponse:
        found_review = self.review_repository.find_by_id(review_id)
        if found_review is None:
            raise ValueError(f"Review id {review_id} not found")
        if found_review.user_id != request.user_id:
            raise ValueError(f"User id {request.user_id} does not belong to this review")
        self.review_repository.delete(review_id)
        delete_response = DeleteReviewResponse(status="Deleted successfully")
        return delete_response

    def get_user_reviews(self, user_id)->List[Review]:
        found_user = self.user_repo.find_by_id(user_id)
        if found_user is None:
            raise ValueError("User does not exist")
        return self.review_repository.find_all()



