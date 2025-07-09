"""
In this module we define the logic of how our facade works,
the connection with the 'database', and the responses to the API.
"""
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.models.reserva import Reserva
from datetime import datetime



class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.review_repo = SQLAlchemyRepository(Review)
        self.reserva_repo = SQLAlchemyRepository(Reserva)

#🧔‍♂️ =================== USERS ===================
    def create_user(self, user_data):
        email = user_data.get('email', '').strip()
        if not email:
            return {'error': 'Email is required'}

        existing_user = self.get_user_by_email(email)
        if existing_user:
            return {'error': 'Email already registered'}

        user = User(**user_data)
        self.user_repo.add(user)
        return user.to_dict()


    def get_users(self):
        users = self.user_repo.get_all()
        return [user.to_dict() for user in users]


    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if user:
            return user.to_dict()
        return None

    def update_user(self, user_id, update_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        new_email = update_data.get('email')
        if new_email and new_email.strip() != user.email:
            existing_user = self.user_repo.get_by_attribute('email', new_email.strip())
            if existing_user and existing_user.id != user.id:
                return {'error': 'Email already registered'}
            user.email = new_email.strip()
            update_data.pop('email')

        if 'password' in update_data:
            user.password = update_data.pop('password')

        user.update(update_data)

        self.user_repo.update(user.id, {})

        return user.to_dict()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def delete_user(self, user_id):
        self.get_user(user_id)
        self.user_repo.delete(user_id)
        return {'massasge': 'user deleted successfully'}
        


#🛜 =================== AMENITIES ===================
    def create_amenity(self, amenity_data):
        place_id = amenity_data.get('place_id')
        name = amenity_data.get('name', '').strip().lower()

        if not name:
            return {'error': 'Amenity name is required'}
        if not place_id or not self.place_repo.get(place_id):
            return {'error': 'Invalid or missing place_id'}

        # Buscar amenity existente
        existing_amenity = self.amenity_repo.get_by_attribute('name', name)

        if existing_amenity:
            # Asociar si no está ya asociado
            place = self.place_repo.get(place_id)
            if existing_amenity in place.amenities:
                return {
                    'message': 'Amenity already exists and is associated with this place',
                    'amenity': existing_amenity.to_dict(),
                    'created': False
                }
            place.amenities.append(existing_amenity)
            self.place_repo.update(place.id, {})
            return {
                'message': 'Amenity already existed, now associated to place',
                'amenity': existing_amenity.to_dict(),
                'created': False,
            }

        # Crear nuevo amenity
        new_amenity = Amenity(name=name)
        self.amenity_repo.add(new_amenity)

        # Asociarlo al place
        place = self.place_repo.get(place_id)
        place.amenities.append(new_amenity)
        self.place_repo.update(place.id, {})

        return {
            'message': 'Amenity created and associated to place',
            'amenity': new_amenity.to_dict(),
            'created': True
            
        }


    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            return amenity.to_dict()
        return None

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [amenity.to_dict() for amenity in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}

        name = amenity_data.get('name')
        if name is not None:
            name = name.strip()
            if not name:
                return {'error': 'Amenity name cannot be empty'}
            amenity_data['name'] = name

        amenity.update(amenity_data)
        self.amenity_repo.update(amenity.id, {})
        return amenity.to_dict()

    def get_amenity_by_name(self, name):
        amenity = self.amenity_repo.get_by_attribute('name', name)
        if amenity:
            return amenity.to_dict()
        return None

#🏠 =================== PLACES ===================
    def create_place(self, place_data):
        price = place_data['price']
        lat = place_data['latitude']
        lon = place_data['longitude']

        # Validaciones básicas
        if price < 0:
            raise ValueError('Invalid price')
        if not -90.0 <= lat <= 90.0:
            raise ValueError('Invalid latitude')
        if not -180.0 <= lon <= 180.0:
            raise ValueError('Invalid longitude')
        
        # Validar existencia de usuario
        owner_id = place_data['owner_id']
        owner = self.user_repo.get(owner_id)
        if not owner:
            return {'error': 'owner_id not found'}

        place = Place(**place_data)
        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)    
        if not place:
            return None

        amenities = place.amenities

        place_dict = place.to_dict()
        place_dict['amenities'] = [
            {'id': amenity.id, 'name': amenity.name} for amenity in amenities
        ] if amenities else []

        return place_dict

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
            return place.to_dict()
        return None

    def get_places_ubis(self):
        places = self.place_repo.get_all()
        return [place.to_ubication() for place in places]

    def add_amenity_to_place(self, place_id, amenity_data):
        name = amenity_data.get('name', '').strip()
        if not name:
            return {'error': 'Amenity name is required'}

        existing = self.amenity_repo.get_by_attribute('name', name)
        if existing and existing.place_id == place_id:
            return {'error': 'Amenity already exists for this place'}

        place = self.place_repo.get(place_id)
        if not place:
            return {'error': 'Place not found'}

        amenity = Amenity(name=name, place_id=place_id)
        self.amenity_repo.add(amenity)

        return amenity.to_dict()

#📝 =================== REVIEWS ===================
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
    

# =================== reserva ===================
    def create_reserva(self, data):
        check_in = datetime.fromisoformat(data['check_in'])
        check_out = datetime.fromisoformat(data['check_out'])

        if check_in >= check_out:
            return {'error': 'La fecha de check-in debe ser anterior a check-out'}

        place = self.place_repo.get(data['place_id'])
        if not place:
            return {'error': 'Lugar no encontrado'}

        user = self.user_repo.get(data['user_id'])
        if not user:
            return {'error': 'Usuario no encontrado'}

        dias = (check_out - check_in).days
        price = int(place.price)
        precio_total = dias * price
        ubicacion = f"{place.latitude}, {place.longitude}"

        reserva = Reserva(
            place_id=place.id,
            user_id=user.id,
            check_in=check_in,
            check_out=check_out,
            precio=precio_total,
            ubicacion=ubicacion
        )


        self.reserva_repo.add(reserva)
        return reserva
