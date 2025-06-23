"""
in this module we define the logic about work our facade, the
connection with the 'database' and the responses to the api
"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    """ USERS """
    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_users(self):
        users = self.user_repo.get_all()
        return [user.to_dict() for user in users]

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, update_data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(update_data)
            return user.to_dict()
        return None

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)


    """ AMENITIES     #######################################"""
    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
    # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
    # Placeholder for logic to retrieve all amenities
        amenities = self.amenity_repo.get_all()
        return [amenity.to_dict() for amenity in amenities]

    def update_amenity(self, amenity_id, amenity_data):
    # Placeholder for logic to update an amenity
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity.to_dict()
        return None

    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute('name', name)


    """ PLACES     #########################################"""
    def create_place(self, place_data):
        price = place_data['price']
        lat = place_data['latitude']
        lon = place_data['longitude']
        if price < 0:
            return {'error': 'invalid price'}
        elif not -90.0 <= lat <= 90.0:
            return {'error': 'invalid latitude'}
        elif not -180.0 <= lon <= 180.0:
            return {'error': 'invalid longitude'}
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
    # Placeholder for logic to retrieve all places
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    def add_amenities(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id['id'])
        return place.add_amenity(amenity)


    def update_place(self, place_id, place_data):
    # Placeholder for logic to update a place
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
            return place.to_dict()
        return None

    def get_places_ubis(self):
        places = self.place_repo.get_all()
        return [place.to_ubication() for place in places]


    """REVIEWS #############################################"""

    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        user = self.user_repo.get(user_id)
        if not user:
            return None
        place = self.place_repo.get(place_id)
        if not place:
            return None
        review = Review(**review_data)
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
    # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
    # Placeholder for logic to retrieve all reviews
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews]

    def get_reviews_by_place(self, place_id):
    # Placeholder for logic to retrieve all reviews for a specific place
        place = self.place_repo.get(place_id)
        reviews = place.reviews
        return [review.to_dict() for review in reviews]

    def update_review(self, review_id, review_data):
    # Placeholder for logic to update a review
        review = self.review_repo.get(review_id)
        if review:
            review.update(review_data)
            return review.to_dict()
        return None

    def delete_review(self, review_id):
    # Placeholder for logic to delete a review
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return None

