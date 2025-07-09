"""Módulo que implementa las reservas"""

from app.models.base_model import BaseModel
import uuid
from datetime import datetime
from app.extensions import db

class Reserva(BaseModel):
    __tablename__ = 'reserva'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    place_id = db.Column(db.String, db.ForeignKey('place.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)

    precio_ = db.Column("precio", db.Float, nullable=False)
    ubicacion_ = db.Column("ubicacion", db.String(128), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='reservas')
    place = db.relationship('Place', backref='reservas')

    def __init__(self, **kwargs):
        if 'precio' in kwargs:
            kwargs['precio_'] = kwargs.pop('precio')
        if 'ubicacion' in kwargs:
            kwargs['ubicacion_'] = kwargs.pop('ubicacion')
        super().__init__(**kwargs)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "place_id": self.place_id,
            "user_id": self.user_id,
            "check_in": self.check_in.isoformat() if self.check_in else None,
            "check_out": self.check_out.isoformat() if self.check_out else None,
            "precio": self.precio_,
            "ubicacion": self.ubicacion_,
        })
        return base

