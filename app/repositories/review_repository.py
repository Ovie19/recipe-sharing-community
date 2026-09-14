from typing import Optional, List
from uuid import UUID

from sqlmodel import Session, select

from app.models.review import Review


class ReviewRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, review: Review) -> Review:
        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)
        return review

    def find_by_id(self, review_id: UUID) -> Optional[Review]:
        statement = select(Review).where(Review.id == str(review_id))
        return self.session.exec(statement).first()

    def update(self, review_id: UUID, data: dict) -> Optional[Review]:
        review = self.find_by_id(review_id)

        if not review:
            return None

        for key, value in data.items():
            if value is not None and hasattr(review, key):
                setattr(review, key, value)

        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)

        return review

    def find_all(self) -> List[Review]:
        statement = select(Review)
        return self.session.exec(statement).all()

    def delete(self, review_id: UUID) -> None:
        review = self.find_by_id(review_id)

        if review:
            self.session.delete(review)
            self.session.commit()

    def clear(self) -> None:
        statement = select(Review)
        results = self.session.exec(statement).all()

        for review in results:
            self.session.delete(review)

        self.session.commit()

    def count(self) -> int:
        statement = select(Review)
        return len(self.session.exec(statement).all())