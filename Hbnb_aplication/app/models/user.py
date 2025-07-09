#!/usr/bin/python3
"""
in this module we define the class User(), the template
of all future entities
"""
from app.extensions import bcrypt
from app.models.base_model import BaseModel
from app.extensions import db
from datetime import datetime
import uuid

class User(BaseModel):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()),nullable=False)
    
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column("password", db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    
    reviews = db.relationship("Review", backref="user", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        password = kwargs.pop('password', None)
        super().__init__(**kwargs)
        if password:
            self.password = password
        if 'is_admin' not in kwargs:
            self.is_admin = False

    @property
    def password(self):
        return None

    @password.setter
    def password(self, raw_password):
        self._password_hash = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return base
