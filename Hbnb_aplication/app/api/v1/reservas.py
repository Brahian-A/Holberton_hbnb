"""Este módulo define las operaciones relacionadas con las reservas."""

from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('reservas', description='Operaciones sobre reservas')

# Modelo para crear una reserva
reserva_create_model = api.model('ReservaCreate', {
    'place_id': fields.String(required=True, description='ID del lugar'),
    'user_id': fields.String(required=True, description='ID del usuario'),
    'check_in': fields.String(required=True, description='Fecha de entrada (YYYY-MM-DD)'),
    'check_out': fields.String(required=True, description='Fecha de salida (YYYY-MM-DD)'),
})

# Modelo de respuesta
reserva_model = api.model('Reserva', {
    'id': fields.String,
    'place_id': fields.String,
    'user_id': fields.String,
    'check_in': fields.String,
    'check_out': fields.String,
    'precio': fields.Float,
    'ubicacion': fields.String,
})

@api.route('/')
class ReservaList(Resource):
    @api.expect(reserva_create_model, validate=True)
    @api.response(201, 'Reserva creada correctamente', reserva_model)
    @api.response(400, 'Datos inválidos')
    def post(self):
        "created a new reserva"
        data = request.json

        try:
            reserva = facade.create_reserva(data)
            return reserva.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
