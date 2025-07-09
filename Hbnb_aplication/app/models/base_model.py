"""
in this module we define the BaseModel(),
like him name say, is the base of all models in
this package, her in charge of generate all id of
the different entities that inherit of her, save and
update all entities
"""
import uuid
from datetime import datetime
from app.extensions import db 

import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True 

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    def save(self):
        """Guarda el modelo y actualiza el timestamp"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Actualiza los atributos desde un diccionario"""
        protected_fields = {'id', 'created_at', 'updated_at'}
        for key, value in data.items():
            if hasattr(self, key) and key not in protected_fields:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        def safe_isoformat(dt):
            return dt.isoformat() if dt else None
    
        return {
            'id': self.id,
            'created_at': safe_isoformat(self.created_at),
            'updated_at': safe_isoformat(self.updated_at),
        }
