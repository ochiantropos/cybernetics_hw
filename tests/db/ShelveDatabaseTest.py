import unittest
from db.database import ShelvePersistence
from db.sequence import IncrementalSequenceStrategy
import os


class Player:

    def __init__(self, name, surname, pk=None):
        self.name = name
        self.surname = surname
        if pk is not None:
            self.pk = pk


class ShelvePersistenceTest(unittest.TestCase):

    repository = None
    sequence = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = ShelvePersistence("players_test", IncrementalSequenceStrategy)
        cls.sequence = cls.repository.sequence_strategy

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.repository
        cls.remove_test_db_files()

    @staticmethod
    def remove_test_db_files():
        my_dir = os.path.join(os.path.dirname(__file__), "../../data/")
        for file_name in os.listdir(my_dir):
            if file_name.startswith("players_test"):
                os.remove(os.path.join(my_dir, file_name))

    def test_save(self):
        player = Player("John", "Doe")
        player = self.repository.save(player)
        self.assertTrue(hasattr(player, 'pk'))
        self.assertEqual(player.pk, self.sequence.get_current())

    def test_save_all(self):
        players = [Player("John1", "Doe1"), Player("John2", "Doe2"), Player("John3", "Doe3"), Player("John4", "Doe4")]
        self.repository.save_all(players)
        for player in players:
            self.assertTrue(hasattr(player, 'pk'))
            self.assertNotEqual(player.pk, 0)

    def test_get_by_id(self):
        player = Player("IdTest", "Test")
        self.repository.save(player)
        retrieved_player = self.repository.get_by_id(player.pk)
        self.assertEqual(player.pk, retrieved_player.pk)
        self.assertEqual(player.name, retrieved_player.name)
        self.assertEqual(player.surname, retrieved_player.surname)

    def test_get_all(self):
        self.remove_test_db_files()
        self.repository.refresh_persistence()
        players = [Player("John1", "Doe1"), Player("John2", "Doe2"), Player("John3", "Doe3"), Player("John4", "Doe4"),
                   Player("John5", "Doe5")]
        self.repository.save_all(players)
        retrieved_players = self.repository.get_all()
        self.assertEqual(len(players), len(retrieved_players))

    def test_delete_by_id(self):
        player = Player("John", "Doe")
        self.repository.save(player)
        self.repository.delete_by_id(player.pk)
        deleted_player = self.repository.get_by_id(player.pk)
        self.assertIsNone(deleted_player)

    def test_sync(self):
        player = Player("Sync", "Sync")
        self.repository.save(player)
        not_synced_player = Player("John", "Doe", player.pk)
        synced_player = self.repository.sync(not_synced_player)
        self.assertEqual(player.pk, synced_player.pk)
        self.assertEqual(player.name, synced_player.name)
        self.assertEqual(player.surname, synced_player.surname)



