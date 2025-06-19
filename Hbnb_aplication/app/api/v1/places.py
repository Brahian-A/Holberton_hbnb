"""
in this module we define and handler all about the data received
of the client since the diferents routes of our web app
"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Ubication already registred')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # Placeholder for the logic to register a new place
        place_data = api.payload

        ubications = facade.get_places_ubis()
        ubication = {
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude']
        }
        if ubication in ubications:
            return {'error': 'Ubication already registred'}, 400
        n_plc = facade.create_place(place_data)
        if isinstance(n_plc, dict):
            return n_plc, 400
        else:
            return {
                "id": n_plc.id,
                "title": n_plc.title,
                "description": n_plc.description,
                "price": n_plc.price,
                "latitude": n_plc.latitud,
                "longitude": n_plc.longitud,
                "owner_id": n_plc.owner_id
            }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        places = facade.get_all_places()
        return places, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID, including associated owner and amenities
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        user = facade.get_user(place.owner_id)
        user = user.to_dict()
        return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitud,
                "longitude": place.longitud,
                "owner": user
            }

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Internal error')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        update_data = api.payload
        place = facade.get_place(place_id)
        if place is None:
            return {'error': 'Place not found'}, 404
        if 'latitude' in update_data and update_data['latitude'] != place.latitud:
            return {'error': "the ubication can't are modify"}, 400
        if 'longitude' in update_data and update_data['longitude'] != place.longitud:
            return {'error': "the ubication can't are modify"}, 400
        update_place = facade.update_place(place_id, update_data)
        if update_place:
            return {"message": "Place updated successfully"}, 200
        else:
            return {'error': 'internal error'}, 500
