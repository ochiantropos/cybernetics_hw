from abc import ABC, abstractmethod
from services.services import *
from models.models import *
from datetime import datetime

_user_service = UserService()
_room_service = RoomService()


class AbstractCommand(ABC):

    @abstractmethod
    def execute(self):
        pass


class LoginCommand(AbstractCommand):

    user_service = _user_service

    def execute(self):
        login = input("Enter login:")
        password = input("Enter password:")
        try:
            self.user_service.login_user(login, password)
        except UserNotFound:
            print("Incorrect login or password")
            return
        print("Successfully logged in")


class RegisterCommand(AbstractCommand):

    user_service = _user_service

    def execute(self):
        login = input("Enter login:")
        password = input("Enter password:")
        try:
            self.user_service.register_user(User(login, password))
        except UserAlreadyExists:
            print(f"User with login {login} already exists")
            return
        print("Successfully registered user")


class ProfileCommand(AbstractCommand):

    user_service = _user_service

    def execute(self):
        user = self.user_service.get_current_user()
        print("Your profile")
        print(f"Login: {user.login}")
        print(f"Balance: {user.balance} \n")


class LogoutCommand(AbstractCommand):

    user_service = _user_service

    def execute(self):
        self.user_service.logout()
        print("Logout successful")


class AddBalanceCommand(AbstractCommand):

    user_service = _user_service

    def execute(self):
        amount = int(input("Enter money amount:"))
        self.user_service.add_balance(amount)


class ListRoomsCommand(AbstractCommand):

    room_service = _room_service

    def execute(self):
        rooms = self.room_service.get_all_rooms()
        rooms.sort(key=lambda val: val.room_name)
        print("------------------------------------")
        for room in rooms:
            print(f"Room number: {room.room_number}")
            print(f"Room name: {room.room_name}")
            print(f"Room capacity: {room.room_capacity}")
            print(f"Room price: {room.room_price}")
            if len(room.booked_dates) != 0:
                print("Booked dates: ")
                for rr in room.booked_dates:
                    print(f"Check in Date: {rr.check_in_date.date()}, Check out Date: {rr.check_out_date.date()}")
            print("------------------------------------")


class BookRoomCommand(AbstractCommand):

    room_service = _room_service

    def execute(self):
        room_number = int(input("Enter room number:"))
        check_in_date = datetime.strptime(input("Enter check in date:"), "%d-%m-%Y")
        check_out_date = datetime.strptime(input("Enter check out date:"), "%d-%m-%Y")
        try:
            self.room_service.book_room(room_number, check_in_date, check_out_date)
        except BookingDateIntersection:
            print("Booking date overlaps with existing ones")
            return
        except NotEnoughMoney:
            print("You have not enough money to book this room for given dates")
            return
        print(f"Successfully booked room {room_number} on dates {check_in_date.date()} to {check_out_date.date()}")
