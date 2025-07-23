from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository

class AmenityService:
    def __init__(self):
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)

    def _associate_amenity_to_place(self, amenity, place):
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            self.place_repo.update(place.id, {})

    def create_amenity(self, amenity_data):
        place_id = amenity_data.get('place_id')
        name = amenity_data.get('name', '').strip().lower()

        if not name:
            return {'error': 'Amenity name is required'}

        place = self.place_repo.get(place_id)
        if not place:
            return {'error': 'Invalid or missing place_id'}

        existing_amenity = self.amenity_repo.get_by_attribute('name', name)

        if existing_amenity:
            if existing_amenity in place.amenities:
                return {
                    'message': 'Amenity already exists and is associated with this place',
                    'amenity': existing_amenity.to_dict(),
                    'created': False
                }
            self._associate_amenity_to_place(existing_amenity, place)
            return {
                'message': 'Amenity already existed, now associated to place',
                'amenity': existing_amenity.to_dict(),
                'created': False,
            }

        new_amenity = Amenity(name=name)
        self.amenity_repo.add(new_amenity)
        self._associate_amenity_to_place(new_amenity, place)

        return {
            'message': 'Amenity created and associated to place',
            'amenity': new_amenity.to_dict(),
            'created': True
        }

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        return amenity.to_dict() if amenity else None

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [amenity.to_dict() for amenity in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}

        name = amenity_data.get('name')
        if name is not None:
            name = name.strip().lower()
            if not name:
                return {'error': 'Amenity name cannot be empty'}

            existing = self.amenity_repo.get_by_attribute('name', name)
            if existing and existing.id != amenity.id:
                return {'error': 'Amenity name already in use'}

            amenity_data['name'] = name

        amenity.update(amenity_data)
        self.amenity_repo.update(amenity.id, {})
        return amenity.to_dict()

    def get_amenity_by_name(self, name):
        name = name.strip().lower()
        amenity = self.amenity_repo.get_by_attribute('name', name)
        return amenity.to_dict() if amenity else None

    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
        self.amenity_repo.delete(amenity_id)
        return True
