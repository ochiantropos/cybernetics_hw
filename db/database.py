from abc import ABC, abstractmethod
import shelve
from .sequence import AbstractSequence
import os


class AbstractDatabase(ABC):

    def __init__(self, db_name):
        self.db_name = db_name

    @abstractmethod
    def write(self, obj):
        pass

    @abstractmethod
    def write_all_objects(self, obj_list):
        pass

    @abstractmethod
    def get_obj_by_id(self, pk):
        pass

    @abstractmethod
    def get_all_objects(self):
        pass

    @abstractmethod
    def delete_obj_by_id(self, pk):
        pass

    @abstractmethod
    def sync_obj(self, obj):
        pass


class ShelveDatabase(AbstractDatabase):
    data_folder = os.path.join(os.path.dirname(__file__), "../data/")

    def __init__(self, db_name: str, sequence_strategy: AbstractSequence.__class__):
        super().__init__(db_name)
        self.sequence_strategy_cls = sequence_strategy
        self.sequence_strategy = sequence_strategy(self.get_last_id())

    def write(self, obj):
        with self._open_db() as db:
            return self._write(obj, db)

    def write_all_objects(self, obj_list):
        with self._open_db() as db:
            for obj in obj_list:
                self._write(obj, db)

    # TODO: throw exception instead of returning None
    def get_obj_by_id(self, pk):
        with self._open_db() as db:
            if self._id_exists(pk, db):
                return self._get_obj(pk, db)
            else:
                return None

    def get_all_objects(self):
        with self._open_db() as db:
            keys = set(db.keys())
            objects = []
            for k in keys:
                objects.append(self._get_obj(k, db))
            return objects

    # TODO: throw exception instead of passing
    def delete_obj_by_id(self, pk):
        with self._open_db() as db:
            if self._id_exists(pk, db):
                self._delete_obj(pk, db)
            else:
                pass

    # TODO: throw exception instead of doing nothing
    def sync_obj(self, obj):
        if self._is_new(obj):
            return obj
        else:
            with self._open_db() as db:
                if self._id_exists(obj.pk, db):
                    return self._get_obj(obj.pk, db)
                else:
                    # TODO: throw exception
                    return None

    def _delete_obj(self, pk, db):
        del db[str(pk)]

    def _write(self, obj, db):
        if self._is_new(obj):
            pk = self.sequence_strategy.next()
            self._set_id(obj, pk)
            db[str(pk)] = obj
            return obj
        else:
            db[str(obj.pk)] = obj
            return obj

    def _get_obj(self, pk, db):
        obj = db[str(pk)]
        self._set_id(obj, pk)
        return obj

    @staticmethod
    def _is_new(obj):
        return not hasattr(obj, 'pk')

    @staticmethod
    def _id_exists(pk, db):
        return str(pk) in db

    @staticmethod
    def _set_id(obj, pk):
        setattr(obj, 'pk', pk)

    def _open_db(self):
        return shelve.open(self.data_folder + self.db_name, "c")

    def get_last_id(self):
        with self._open_db() as db:
            keys = set(map(int, db.keys()))
            if len(keys) == 0:
                return self.sequence_strategy_cls.min_value()
            return max(keys)
