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
        try:
            check_in = datetime.fromisoformat(data['check_in'])
            check_out = datetime.fromisoformat(data['check_out'])
        except ValueError:
            raise ValueError("Formato de fecha inválido. Debe ser YYYY-MM-DD.")

        if check_in >= check_out:
            raise ValueError('La fecha de check-in debe ser anterior a check-out')

        place = self.place_repo.get(data['place_id'])
        if not place:
            raise ValueError('Lugar no encontrado')

        user = self.user_repo.get(data['user_id'])
        if not user:
            raise ValueError('Usuario no encontrado')

        reservas_existentes = self.reserva_repo.filter_by_place_and_date_range(
            place_id=place.id,
            check_in=check_in,
            check_out=check_out
        )
        if reservas_existentes:
            raise ValueError('Ya existe una reserva para ese lugar en las fechas indicadas.')

        dias = (check_out - check_in).days
        precio_total = dias * int(place.price)
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
        return reserva

