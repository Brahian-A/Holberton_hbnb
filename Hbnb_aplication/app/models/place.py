#!/usr/bin/python3
"""
Define the class Place, with SQLAlchemy support and relationships.
"""
from app.models.base_model import BaseModel
from app.extensions import db
import uuid
from datetime import datetime

# Tabla intermedia para relación muchos-a-muchos con amenities
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String, db.ForeignKey('place.id'), primary_key=True),
    db.Column('amenity_id', db.String, db.ForeignKey('amenity.id'), primary_key=True)
)

class Place(BaseModel):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.String(50))

    #relaciones
    owner = db.relationship("User", backref="places")
    reviews = db.relationship("Review", backref="place", cascade="all, delete-orphan")
    amenities = db.relationship("Amenity", secondary=place_amenity, backref="places")
    

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'title': self.title,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'description': self.description,
            'price': getattr(self, 'price', None),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'amenities': [a.to_dict() for a in self.amenities],
            'reviews': [r.to_dict() for r in self.reviews]
        })
        return base

    def to_ubication(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude
        }
