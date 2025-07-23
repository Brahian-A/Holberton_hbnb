from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class PlaceService:
    def __init__(self):
        self.place_repo = SQLAlchemyRepository(Place)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.user_repo = SQLAlchemyRepository(User)

    def create_place(self, place_data):
        price = place_data['price']
        lat = place_data['latitude']
        lon = place_data['longitude']

        # Validaciones básicas
        if price < 0:
            return {'error': 'Price must be non-negative'}
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
            return {'error': 'Place not found'}

        user = place.owner
        amenities = place.amenities

        place_dict = place.to_dict()
        place_dict['owner_id'] = {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name}
        place_dict['amenities'] = [
            {'id': amenity.id, 'name': amenity.name} for amenity in amenities
        ] if amenities else []

        return place_dict

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return {'error': 'Place not found'}

        if 'price' in place_data and place_data['price'] < 0:
            return {'error': 'Price must be non-negative'}
        
        if 'latitude' in place_data:
            lat = place_data['latitude']
            if not -90.0 <= lat <= 90.0:
                return {'error': 'Invalid latitude'}
        
        if 'longitude' in place_data:
            lon = place_data['longitude']
            if not -180.0 <= lon <= 180.0:
                return {'error': 'Invalid longitude'}

        updated_place = self.place_repo.update(place_id, place_data)
        if updated_place:
            return updated_place.to_dict()
        
        # Por si algo raro pasa
        return {'error': 'Failed to update place'}


    def get_places_ubis(self):
        places = self.place_repo.get_all()
        return [place.to_ubication() for place in places]

    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        if not place:
            return {'error': 'Place not found'}

        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}

        if amenity in place.amenities:
            return {'message': 'Amenity already associated with this place'}

        place.amenities.append(amenity)
        self.place_repo.update(place.id, {})

        return {'message': 'Amenity added to place', 'amenity': amenity.to_dict()}
    
    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return {'error': 'Place not found'}

        self.place_repo.delete(place_id)
        return {'message': 'Place deleted successfully'}