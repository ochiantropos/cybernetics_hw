class User:

    def __init__(self, login, password, balance=0, pk=None):
        self.login = login
        self.password = password
        self.balance = balance
        if pk is not None:
            self.pk = pk


class RoomRecord:

    def __init__(self, user_pk: int, check_in_date, check_out_date):
        self.user_pk = user_pk
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date


class Room:

    def __init__(self, room_number: int, room_name: str, room_price: int, room_capacity: int, booked_dates: list[RoomRecord], pk=None):
        self.room_number = room_number
        self.room_name = room_name
        self.room_price = room_price
        self.room_capacity = room_capacity
        self.booked_dates = booked_dates
        if pk is not None:
            self.pk = pk
