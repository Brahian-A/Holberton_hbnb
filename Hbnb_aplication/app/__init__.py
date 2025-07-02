"""
in this module we init the app package
"""
from flask import Flask, render_template
from flask_restx import Api
from app.extensions import bcrypt, jwt, db

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

def create_app(config_class):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)
    app.config['JWT_SECRET_KEY'] = 'mi-clave-supersecreta'

    # Inicialización de extensiones
    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

        # Ruta pagina principal
    @app.route('/')
    def index():
        "sirve la pagina principal index.html"
        return render_template('index.html')

    # API RESTX
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/docs/')

    # Rutas
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
