from app.models.user import User
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository

class UserService:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)

    def create_user(self, user_data):
        email = user_data.get('email', '').strip()
        if not email:
            return {'error': 'Email is required'}

        if self.user_repo.get_by_attribute('email', email):
            return {'error': 'Email already registered'}

        user = User(**user_data)
        self.user_repo.add(user)
        return user.to_dict()

    def get_users(self):
        return [user.to_dict() for user in self.user_repo.get_all()]

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        return user.to_dict() if user else None

    def update_user(self, user_id, update_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        new_email = update_data.get('email')
        if new_email and new_email.strip() != user.email:
            existing = self.user_repo.get_by_attribute('email', new_email.strip())
            if existing and existing.id != user.id:
                return {'error': 'Email already registered'}
            user.email = new_email.strip()
            update_data.pop('email')

        if 'password' in update_data:
            user.password = update_data.pop('password')

        user.update(update_data)
        self.user_repo.update(user.id, {})
        return user.to_dict()

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return {'error': 'User not found'}

        places = self.place_repo.get_all_by_attribute('owner_id', user_id)
        if places:
            return {
                'error': 'User has active places and cannot be deleted',
                'places': [place.to_dict() for place in places]
            }

        deleted = self.user_repo.delete(user_id)
        if not deleted:
            return {'error': 'User not found or could not be deleted'}

        return {'message': 'User deleted successfully'}



    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
