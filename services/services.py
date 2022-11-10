from db.database import ShelveRepository
from session.holder import SessionHolder
from .exceptions import *
from models.models import *
from utils.date import intersects

_user_repository = ShelveRepository("users")
_room_repository = ShelveRepository("rooms")


class UserService:
    repository = _user_repository

    def register_user(self, new_user) -> User:
        users = self.repository.get_all()
        for user in users:
            if user.login == new_user.login:
                raise UserAlreadyExists(new_user.login)
        return self.repository.save(new_user)

    def login_user(self, login, password):
        users = self.repository.get_all()
        for user in users:
            if user.login == login and user.password == password:
                SessionHolder.set_current_user(user)
                return
        raise UserNotFound(login)

    def add_balance(self, amount: int) -> User:
        user = SessionHolder.get_current_user()
        user.balance += amount
        return self.repository.save(user)

    def get_current_user(self) -> User:
        return self.repository.sync(SessionHolder.get_current_user())

    def logout(self):
        SessionHolder.set_current_user(None)


class RoomService:
    room_repository = _room_repository

    user_repository = _user_repository

    def get_all_rooms(self) -> list[Room]:
        return self.room_repository.get_all()

    def book_room(self, room_pk, check_in_date, check_out_date):
        user = SessionHolder.get_current_user()
        room_record = RoomRecord(user.pk, check_in_date, check_out_date)
        room = self.room_repository.get_by_id(room_pk)
        date_diff = abs((check_out_date - check_in_date).days)
        if user.balance < room.room_price * date_diff:
            raise NotEnoughMoney()
        for rr in room.booked_dates:
            if intersects(check_in_date, check_out_date, rr.check_in_date, rr.check_out_date):
                raise BookingDateIntersection()
        room.booked_dates.append(room_record)
        user.balance -= room.room_price * date_diff
        self.user_repository.save(user)
        self.room_repository.save(room)
