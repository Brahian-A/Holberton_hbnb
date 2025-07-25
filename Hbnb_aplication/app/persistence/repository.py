"""
in this module we define what would
be the improvise data base
"""
from abc import ABC, abstractmethod
from app.extensions import db
from sqlalchemy import and_

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

# ===================== IN-MEMORY =====================

class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

    def get_by_place_id(self, place_id):
        return [obj for obj in self._storage.values() if getattr(obj, 'place_id', None) == place_id]

    def get_reviews_by_place(self, place_id):
        return [obj for obj in self._storage.values() if getattr(obj, 'place_id', None) == place_id]

# ===================== SQLALCHEMY =====================

class SQLAlchemyRepository(Repository):
    def __init__(self, model_class):
        self.model_class = model_class

    def add(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def get(self, obj_id):
        return self.model_class.query.get(obj_id)

    def get_all(self):
        return self.model_class.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return False  
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def get_by_attribute(self, attr_name, attr_value):
        return self.model_class.query.filter(
            getattr(self.model_class, attr_name) == attr_value
        ).first()

    def get_reviews_by_place(self, place_id):
        return self.model_class.query.filter_by(place_id=place_id).all()

    def get_all_by_attribute(self, attr_name, attr_value):
        return self.model_class.query.filter(getattr(self.model_class, attr_name) == attr_value).all()
    
    def filter_by_place_and_date_range(self, place_id, check_in, check_out):
        return self.model_class.query.filter(
            self.model_class.place_id == place_id,
            and_(
                self.model_class.check_in < check_out,
                self.model_class.check_out > check_in
            )
        ).all()