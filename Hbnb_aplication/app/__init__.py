"""
in this module we init the app package
"""
from flask import Flask
from flask_restx import Api
from app.extensions import bcrypt, jwt, db
from flask import render_template

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.reservas import api as reservas_ns

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['JWT_SECRET_KEY'] = 'mi-clave-supersecreta'

    # Inicialización de extensiones
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    # API RESTX
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    
    @app.route('/')
    def index():
        print("Ruta '/' llamada")
        return render_template('index.html')
    
    # Rutas
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(reservas_ns, path='/api/v1/reservas')

    return app
