#!/usr/bin/python3
"""
in this module we define the class Amenity(). the template
of all future instances
"""
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if len(name) < 50:
            self.name = name
        else:
            self.name = None

    def to_dict(self):
        return {'id': self.id, 'name': self.name}