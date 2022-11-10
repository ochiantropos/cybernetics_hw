from db.database import AbstractRepository


class MockRepository(AbstractRepository):

    def save(self, obj):
        pass

    def save_all(self, obj_list):
        pass

    def get_by_id(self, pk):
        pass

    def get_all(self):
        pass

    def delete_by_id(self, pk):
        pass

    def sync(self, obj):
        pass

    def refresh_persistence(self):
        pass
