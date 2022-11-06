class PersistentObjectDoesNotExists(Exception):
    def __init__(self, pk, db_name):
        super().__init__(f"Persistent object of db {db_name} with pk {pk} does not exists")
