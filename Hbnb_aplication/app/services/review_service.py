from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place

class ReviewService:
    def __init__(self):
        self.review_repo = SQLAlchemyRepository(Review)
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)

    def create_review(self, review_data):
        if 'text' not in review_data or not review_data['text']:
            raise ValueError("Review text is required.")

        try:
            rating = float(str(review_data.get('rating')).replace(',', '.'))
        except (ValueError, TypeError):
            raise ValueError("Valid rating is required.")

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])

        if not user or not place:
            raise ValueError("Invalid user_id or place_id.")

        review = Review(
            text=review_data['text'],
            rating=rating,
            user_id=user.id,
            place_id=place.id
        )

        self.review_repo.add(review)
        return review.to_dict()

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review.to_dict()

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews]

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")

        reviews = self.review_repo.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)

        if not review:
            raise ValueError("Review not found.")

        if 'text' in review_data:
            review.text = review_data['text']

        if 'rating' in review_data:
            try:
                rating = float(str(review_data['rating']).replace(',', '.'))
            except (ValueError, TypeError):
                raise ValueError("Valid rating is required.")
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            review.rating = rating

        self.review_repo.update(review.id, {})
        return review.to_dict()

    def delete_review(self, review_id):
        self.get_review(review_id)
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}
