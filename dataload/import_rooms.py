from db.database import ShelveRepository
from models.models import Room

repository = ShelveRepository("rooms")

rooms = [
    Room(1, "Room 1", 100, 2, [], pk=1),
    Room(2, "Room 2", 200, 2, [], pk=2),
    Room(3, "Room 3", 300, 3, [], pk=3),
    Room(4, "Room 4", 400, 3, [], pk=4),
    Room(5, "Room 5", 500, 4, [], pk=5),
    Room(6, "Room 6", 600, 4, [], pk=6),
    Room(7, "Room 7", 700, 6, [], pk=7),
    Room(8, "Room 8", 800, 8, [], pk=8),
]

if __name__ == "__main__":
    repository.save_all(rooms)
