class UserNotFound(Exception):

    def __init__(self, login):
        super().__init__(f"User with login {login} not found")


class UserAlreadyExists(Exception):

    def __init__(self, login):
        super().__init__(f"User with login {login} already exists")


class BookingDateIntersection(Exception):

    def __init__(self):
        super().__init__()


class NotEnoughMoney(Exception):

    def __init__(self):
        super().__init__()