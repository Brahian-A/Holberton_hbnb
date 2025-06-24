"""
in this module we define and handler all about the data received
of the client since the diferents routes of our web app
"""


from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'place_id': fields.String(required=True, description='ID of the place associated')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        name = amenity_data.get('name')
        place_id = amenity_data.get('place_id')

        if not name or not name.strip():
            return {'error': 'Invalid input data: name is required'}, 400
        if not place_id:
            return {'error': 'Invalid input data: place_id is required'}, 400
        
        existing_amenity = facade.get_amenity_by_name(name.strip())
        if existing_amenity:
            return {'error': 'Amenity already registered'}, 400
        
        new_amenity = facade.create_amenity({'name': name.strip(), 'place_id': place_id})

        if 'error' in new_amenity:
            return new_amenity, 400

        return new_amenity, 201

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        updated_data = api.payload

        if not updated_data.get('name'):
            return {'error': 'Invalid input data: name is required'}, 400

        updated_amenity = facade.update_amenity(amenity_id, updated_data)

        if updated_amenity:
            return updated_amenity, 200

        return {'error': 'Amenity not found'}, 404