"""
In this module we define and handle all data received
from the client through the different routes of our web app.
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
        "Create a new amenity"
        amenity_data = api.payload
        result = facade.create_amenity(amenity_data)
        if isinstance(result, dict) and 'error' in result:
            return result, 400
        return result, 201 if result.get('created', False) else 200

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        "Get all amenities"
        amenities = facade.get_all_amenities()
        return amenities, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        "Get amenity by ID"
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity, 200

    @api.expect(amenity_update_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        "Update amenity"
        updated_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, updated_data)
        if updated_amenity:
            return updated_amenity, 200
        return {'error': 'Amenity not found'}, 404

    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete amenity"""
        result = facade.delete_amenity(amenity_id)
        if 'error' in result:
            return result, 404
        return result, 200