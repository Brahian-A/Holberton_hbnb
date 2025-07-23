from app.models.reserva import Reserva
from app.models.place import Place
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from datetime import datetime

class ReservasService:
    def __init__(self):
        self.reserva_repo = SQLAlchemyRepository(Reserva)
        self.place_repo = SQLAlchemyRepository(Place)
        self.user_repo = SQLAlchemyRepository(User)

    def create_reserva(self, data):
        check_in = datetime.fromisoformat(data['check_in'])
        check_out = datetime.fromisoformat(data['check_out'])

        if check_in >= check_out:
            return {'error': 'La fecha de check-in debe ser anterior a check-out'}

        place = self.place_repo.get(data['place_id'])
        if not place:
            return {'error': 'Lugar no encontrado'}

        user = self.user_repo.get(data['user_id'])
        if not user:
            return {'error': 'Usuario no encontrado'}

        dias = (check_out - check_in).days
        price = int(place.price)
        precio_total = dias * price
        ubicacion = f"{place.latitude}, {place.longitude}"

        reserva = Reserva(
            place_id=place.id,
            user_id=user.id,
            check_in=check_in,
            check_out=check_out,
            precio=precio_total,
            ubicacion=ubicacion
        )


        self.reserva_repo.add(reserva)
        return reserva.to_dict()