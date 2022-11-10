import unittest
from unittest.mock import MagicMock
from mocks.mocks import *
from models.models import *
from services import services
from services.exceptions import *
from session.holder import SessionHolder
from datetime import datetime


class UserServiceTest(unittest.TestCase):
    user_service = services.UserService()
    mocked_user_data_list = [User("test", "test"), User("test1", "test1")]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user_service.repository = MockRepository("mock")
        cls.user_service.repository.get_all = MagicMock(return_value=cls.mocked_user_data_list)
        cls.user_service.repository.save = MagicMock()

    def tearDown(self) -> None:
        SessionHolder.set_current_user(None)

    def test_creates_user_with_new_login_and_password(self):
        user = User("test2", "test2")
        self.user_service.register_user(user)
        self.user_service.repository.save.assert_called_with(user)

    def test_register_throws_exceptions_given_user_with_existing_login_or_password(self):
        user = User("test", "test")
        self.assertRaises(UserAlreadyExists, self.user_service.register_user, user)

    def test_logins_user(self):
        self.user_service.login_user("test", "test")
        self.assertEqual(SessionHolder.get_current_user().login, self.mocked_user_data_list[0].login)
        self.assertEqual(SessionHolder.get_current_user().password, self.mocked_user_data_list[0].password)

    def test_login_throws_exception_given_bad_credentials(self):
        self.assertRaises(UserNotFound, self.user_service.login_user, "nonexistent", "nonexistent")
        self.assertIsNone(SessionHolder.get_current_user())

    def test_add_balance_adds_balance(self):
        user = User("Balance", "Test")
        SessionHolder.set_current_user(user)
        self.user_service.add_balance(200)
        self.assertEqual(user.balance, 200)
        self.user_service.add_balance(500)
        self.assertEqual(user.balance, 700)

    def test_logouts(self):
        user = User("Logout", "Test")
        SessionHolder.set_current_user(user)
        self.user_service.logout()
        self.assertIsNone(SessionHolder.get_current_user())


class RoomServiceTest(unittest.TestCase):

    room_service = services.RoomService()
    mocked_room_data = [Room(1, "Room 1", 100, 2, []), Room(2, "Room 2", 200, 2, [])]

    @classmethod
    def setUpClass(cls) -> None:
        cls.room_service.user_repository = MockRepository("mock")
        cls.room_service.room_repository = MockRepository("mock")
        cls.room_service.room_repository.get_all = MagicMock(return_value=cls.mocked_room_data)
        cls.room_service.room_repository.get_by_id = MagicMock(return_value=cls.mocked_room_data[0])
        cls.room_service.room_repository.save = MagicMock()
        cls.room_service.user_repository.save = MagicMock()

    def tearDown(self) -> None:
        SessionHolder.set_current_user(None)
        for room in self.mocked_room_data:
            room.booked_dates = []

    def test_get_all_rooms(self):
        rooms = self.room_service.get_all_rooms()
        self.assertIs(rooms, self.mocked_room_data)

    def test_book_room(self):
        user = User("Book", "Test", 1_000_000, pk=1)
        SessionHolder.set_current_user(user)
        check_in_date = self._string_to_date("08-11-2022")
        check_out_date = self._string_to_date("11-11-2022")
        self.room_service.book_room(1, check_in_date, check_out_date)
        self.assertEqual(user.balance, 1_000_000 - 300)
        self.assertEqual(len(self.mocked_room_data[0].booked_dates), 1)
        self.assertEqual(self.mocked_room_data[0].booked_dates[0].check_in_date, check_in_date)
        self.assertEqual(self.mocked_room_data[0].booked_dates[0].check_out_date, check_out_date)

    def test_book_room_throws_not_enough_money_given_user_with_insufficient_balance(self):
        user = User("Book", "Test", 100, pk=1)
        SessionHolder.set_current_user(user)
        check_in_date = self._string_to_date("08-11-2022")
        check_out_date = self._string_to_date("11-11-2022")
        self.assertRaises(NotEnoughMoney, self.room_service.book_room, 1, check_in_date, check_out_date)
        self.assertEqual(user.balance, 100)
        self.assertEqual(len(self.mocked_room_data[0].booked_dates), 0)

    def test_book_room_throws_date_intersection_given_room_with_overlapping_dates_when_input_overlaps_with_it(self):
        user = User("Book", "Test", 1_000_000, pk=1)
        SessionHolder.set_current_user(user)
        self.mocked_room_data[0].booked_dates = [RoomRecord(1, self._string_to_date("05-11-2022"), self._string_to_date("12-11-2022"))]
        check_in_date = datetime.strptime("08-11-2022", "%d-%m-%Y")
        check_out_date = datetime.strptime("11-11-2022", "%d-%m-%Y")
        self.assertRaises(BookingDateIntersection, self.room_service.book_room, 1, check_in_date, check_out_date)
        self.assertEqual(len(self.mocked_room_data[0].booked_dates), 1)

    @staticmethod
    def _string_to_date(date: str):
        return datetime.strptime(date, "%d-%m-%Y")
