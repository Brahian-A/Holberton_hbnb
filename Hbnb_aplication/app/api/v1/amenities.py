"""
This module defines and handles all the data received from the client
through the different routes of our web app.

Este módulo define y maneja todos los datos recibidos del cliente
a través de las diferentes rutas de nuestra aplicación web.
"""


from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Modelo para crear amenity (POST) con place_id obligatorio
amenity_create_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'place_id': fields.String(required=True, description='ID of the place associated')
})

# Modelo para actualizar amenity (PUT) solo name obligatorio
amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_create_model, validate=True)
    @api.response(201, 'Amenity successfully created or associated')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        # Placeholder for the logic to register a new amenity
        amenity_data = api.payload
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity already registered'}, 400
        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 200

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Placeholder for logic to return a list of all amenities
        amenities = facade.get_all_amenities()
        return amenities, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Placeholder for the logic to retrieve an amenity by ID
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity, 200

    @api.expect(amenity_update_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Placeholder for the logic to update an amenity by ID
        updated_data = api.payload
        if not 'name' in updated_data:
            return {'error': 'Invalid input data'}, 400
        updated_amnty = facade.update_amenity(amenity_id, updated_data)
        if updated_amnty:
            return {"message": "Amenity updated successfully"}, 200
        return {'error': 'Amenity not found'}, 404