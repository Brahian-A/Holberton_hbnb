#!/usr/bin/python3
"""
Define the class Amenity().
"""
from app.models.base_model import BaseModel
from app.extensions import db
import uuid
from datetime import datetime

class Amenity(BaseModel):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    def to_dict(self):
        base = super().to_dict()
        base.update({
            'name': self.name
        })
        return base
