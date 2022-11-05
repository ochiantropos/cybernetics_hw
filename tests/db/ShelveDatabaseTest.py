import unittest
from db.database import ShelveDatabase
from db.sequence import IncrementalSequenceStrategy
import os


class Player:

    def __init__(self, name, surname, pk=None):
        self.name = name
        self.surname = surname
        if pk is not None:
            self.pk = pk


class ShelveDatabaseTest(unittest.TestCase):

    def setUp(self) -> None:
        self.repository = ShelveDatabase("players_test", IncrementalSequenceStrategy)

    def tearDown(self) -> None:
        self.remove_test_db_files()

    @staticmethod
    def remove_test_db_files():
        my_dir = os.path.join(os.path.dirname(__file__), "../../data/")
        for file_name in os.listdir(my_dir):
            if file_name.startswith("players_test"):
                os.remove(os.path.join(my_dir, file_name))

    def test_saves_obj(self):
        player = Player("John", "Doe")
        player = self.repository.write(player)
        self.assertTrue(hasattr(player, 'pk'))
        self.assertEqual(player.pk, 1)

