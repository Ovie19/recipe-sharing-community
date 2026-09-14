import unittest
import uuid
from unittest.mock import Mock

from app.services.review_service import ReviewService
from app.repositories.in_memory_review_repository import InMemoryReviewRepository
from app.models.review import ReviewCreate, ReviewUpdate, DeleteReviewRequest
from app.models.user import User
from app.models.recipe import Recipe
from app.models.recipe import Category



class ReviewTest(unittest.TestCase):
    # user_id = uuid4()
    # recipe_id = uuid4()
    # review_id = uuid4()
    user_id = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
    recipe_id = uuid.UUID("987e6543-e21b-12d3-a456-426614174000")
    review_id = uuid.UUID("7f3c2a91-6e54-4b87-a1d9-3c8e5f204b76")


    def test_review_is_successfully_created(self):
        review_repo = InMemoryReviewRepository()
        user_repo = Mock()
        recipe_repo = Mock()

        user = User(id = self.user_id,username = "test-username",email = "email@test-email.com",password = "hashed_password")
        recipe = Recipe(user_id = self.user_id,
                              name="test recipe",
                              description="test recipe description",
                              ingredients=["ingredient 1", "ingredient 2"],
                              instructions=["instruction 1", "instruction 2"],
                              category=Category.DINNER,
                              preparation_time=10,
                              )

        user_repo.find_by_id.return_value = user
        recipe_repo.find_by_id.return_value = recipe


        review_service = ReviewService(review_repo,user_repo,recipe_repo)
        create_request = ReviewCreate(user_id=self.user_id,
                                      recipe_id=self.recipe_id,
                                      comment="This is a comment")
        review_response = review_service.create_review(create_request)
        self.assertIsNotNone(review_response)
        self.assertEqual(self.review_id, review_response.id)
        user_repo.find_by_id.assert_called_once_with(self.user_id)
        recipe_repo.find_by_id.assert_called_once_with(self.recipe_id)


    def test_update_review_with_valid_credentials_review_updates_successfully(self):
        review_repo = InMemoryReviewRepository()
        user_repo = Mock()
        recipe_repo = Mock()

        review_service = ReviewService(review_repo, user_repo, recipe_repo)
        create_request = ReviewCreate(user_id=self.user_id,
                                      recipe_id=self.recipe_id,
                                      comment="This is a comment")
        review_response = review_service.create_review(create_request)
        update_request = ReviewUpdate(comment="Updated comment")
        review_id = self.review_id
        update_response = review_service.update_review(review_id, update_request)
        self.assertEqual("Updated comment", update_response.comment)

    def test_delete_review_with_valid_credentials_review_gets_deleted_successfully(self):
        review_repo = InMemoryReviewRepository()
        user_repo = Mock()
        recipe_repo = Mock()

        review_service = ReviewService(review_repo, user_repo, recipe_repo)
        create_request = ReviewCreate(user_id=self.user_id,
                                      recipe_id=self.recipe_id,
                                      comment="This is a comment")
        review_service.create_review(create_request)

        delete_request = DeleteReviewRequest(user_id=self.user_id,)
        review_id = self.review_id
        delete_response = review_service.delete_review(review_id,delete_request)
        self.assertEqual("Deleted successfully", delete_response.status)

    def test_get_all_reviews_with_valid_credentials_returns_all_reviews(self):
        review_repo = InMemoryReviewRepository()
        user_repo = Mock()
        recipe_repo = Mock()

        review_service = ReviewService(review_repo, user_repo, recipe_repo)
        create_request = ReviewCreate(user_id=self.user_id,
                                      recipe_id=self.recipe_id,
                                      comment="This is a comment")
        review_service.create_review(create_request)

        user_id = self.user_id
        response = review_service.get_user_reviews(user_id)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)

    def test_create_review_raises_Exception_with_invalid_user_id(self):
        review_repo = InMemoryReviewRepository()
        user_repo = Mock()
        recipe_repo = Mock()

        user = User(id = self.user_id,username = "test-username",email = "email@test-email.com",password = "hashed_password")
        recipe = Recipe(user_id = self.user_id,
                              name="test recipe",
                              description="test recipe description",
                              ingredients=["ingredient 1", "ingredient 2"],
                              instructions=["instruction 1", "instruction 2"],
                              category=Category.DINNER,
                              preparation_time=10,
                              )

        user_repo.find_by_id.return_value = None
        recipe_repo.find_by_id.return_value = recipe


        review_service = ReviewService(review_repo,user_repo,recipe_repo)
        create_request = ReviewCreate(user_id=self.user_id,
                                      recipe_id=self.recipe_id,
                                      comment="This is a comment")
        with self.assertRaises(ValueError):
            review_service.create_review(create_request)

    def test_create_review_raises_Exception_with_invalid_recipe_id(self):
        review_repo = InMemoryReviewRepository()
        user_repo = Mock()
        recipe_repo = Mock()

        user = User(id = self.user_id,username = "test-username",email = "email@test-email.com",password = "hashed_password")
        recipe = Recipe(user_id = self.user_id,
                              name="test recipe",
                              description="test recipe description",
                              ingredients=["ingredient 1", "ingredient 2"],
                              instructions=["instruction 1", "instruction 2"],
                              category=Category.DINNER,
                              preparation_time=10,
                              )

        user_repo.find_by_id.return_value = user
        recipe_repo.find_by_id.return_value = None


        review_service = ReviewService(review_repo,user_repo,recipe_repo)
        create_request = ReviewCreate(user_id=self.user_id,
                                      recipe_id=self.recipe_id,
                                      comment="This is a comment")
        with self.assertRaises(ValueError):
            review_service.create_review(create_request)
        user_repo.find_by_id.assert_called_once_with(self.user_id)

    def test_update_review_with_invalid_review_id_raises_exception(self):
        review_repo = InMemoryReviewRepository()
        user_repo = Mock()
        recipe_repo = Mock()

        review_service = ReviewService(review_repo, user_repo, recipe_repo)


        update_request = ReviewUpdate(comment="Updated comment")
        review_id = self.review_id
        with self.assertRaises(ValueError):
            review_service.update_review(review_id, update_request)

    def test_delete_review_with_invalid_review_id_raises_exception(self):
        review_repo = InMemoryReviewRepository()
        user_repo = Mock()
        recipe_repo = Mock()

        review_service = ReviewService(review_repo, user_repo, recipe_repo)

        delete_request = DeleteReviewRequest(user_id=self.user_id,)
        review_id = self.review_id
        with self.assertRaises(ValueError):
            review_service.delete_review(review_id, delete_request)

    def test_delete_review_with_valid_recipe_id_and_invalid_user_id_raises_exception(self):
        review_repo = InMemoryReviewRepository()
        user_repo = Mock()
        recipe_repo = Mock()

        review_service = ReviewService(review_repo, user_repo, recipe_repo)
        create_request = ReviewCreate(user_id=self.user_id,
                                      recipe_id=self.recipe_id,
                                      comment="This is a comment")
        review_service.create_review(create_request)

        delete_request = DeleteReviewRequest(user_id=self.recipe_id,)
        review_id = self.review_id
        with self.assertRaises(ValueError):
            review_service.delete_review(review_id, delete_request)




if __name__ == '__main__':
    unittest.main()
