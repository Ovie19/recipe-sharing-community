from app.models.review import Review

from typing import Optional, List
from uuid import UUID



class InMemoryReviewRepository:
    def __init__(self):
        self.reviews: List[Review] = []

    def save(self, review: Review) -> Review:
        self.reviews.append(review)
        return review

    def find_by_id(self, review_id: UUID) -> Optional[Review]:
        for review in self.reviews:
            if review.id == review_id:
                return review
        return None

    def update(self, review_id: UUID, data: dict) -> Optional[Review]:
        found_review = self.find_by_id(review_id)
        if found_review is not None:
            updated = found_review.model_copy(update=data)
            index = self.reviews.index(found_review)
            self.reviews[index] = updated
            return updated

        return None

    def find_all(self) -> List[Review]:
        return self.reviews

    def delete(self, review_id:UUID)-> None:
        for review in self.reviews:
            if review.id == review_id:
                self.reviews.remove(review)
        return None

    def clear(self)-> None:
        self.reviews.clear()
        return None

    def count(self)-> int:
        return len(self.reviews)