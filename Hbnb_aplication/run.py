from flask import render_template
from app import create_app
from app.extensions import db
from config import DevelopmentConfig
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.reserva import Reserva
from app.templates import *

app = create_app(DevelopmentConfig)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)