from app.services.user_service import UserService
from app.services.place_service import PlaceService
from app.services.amenity_service import AmenityService
from app.services.review_service import ReviewService
from app.services.reservas_service import ReservasService

class HBnBFacade:
    def __init__(self):
        self.user_service = UserService()
        self.place_service = PlaceService()
        self.amenity_service = AmenityService()
        self.review_service = ReviewService()
        self.reserva_service = ReservasService()

   #🧔‍♂️ =================== USERS ===================
    def create_user(self, user_data):
        return self.user_service.create_user(user_data)

    def get_users(self):
        return self.user_service.get_users()

    def get_user(self, user_id):
        return self.user_service.get_user(user_id)

    def update_user(self, user_id, update_data):
        return self.user_service.update_user(user_id, update_data)

    def get_user_by_email(self, email):
        return self.user_service.get_user_by_email(email)

    def delete_user(self, user_id):
        return self.user_service.delete_user(user_id)

    #🛜 =================== AMENITIES ===================
    def create_amenity(self, amenity_data):
        return self.amenity_service.create_amenity(amenity_data)

    def get_amenity(self, amenity_id):
        return self.amenity_service.get_amenity(amenity_id)

    def get_all_amenities(self):
        return self.amenity_service.get_all_amenities()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_service.update_amenity(amenity_id, amenity_data)

    def get_amenity_by_name(self, name):
        return self.amenity_service.get_amenity_by_name(name)

    def delete_amenity(self, amenity_id):
        return self.amenity_service.delete_amenity(amenity_id)
    #🏠 =================== PLACES ===================
    def create_place(self, place_data):
        return self.place_service.create_place(place_data)

    def get_place(self, place_id):
        return self.place_service.get_place(place_id)

    def get_all_places(self):
        return self.place_service.get_all_places()

    def update_place(self, place_id, place_data):
        return self.place_service.update_place(place_id, place_data)

    def get_places_ubis(self):
        return self.place_service.get_places_ubis()

    def add_amenity_to_place(self, place_id, amenity_data):
        return self.place_service.add_amenity_to_place(place_id, amenity_data)

    #📝 =================== REVIEWS ===================
    def create_review(self, review_data):
        return self.review_service.create_review(review_data)

    def get_review(self, review_id):
        return self.review_service.get_review(review_id)

    def get_all_reviews(self):
        return self.review_service.get_all_reviews()

    def get_reviews_by_place(self, place_id):
        return self.review_service.get_reviews_by_place(place_id)

    def update_review(self, review_id, review_data):
        return self.review_service.update_review(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_service.delete_review(review_id)

    # =================== reserva ===================
    def create_reserva(self, data):
        return self.reserva_service.create_reserva(data)
