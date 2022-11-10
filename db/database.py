from abc import ABC, abstractmethod
import shelve
from .sequence import AbstractSequence, IncrementalSequence
import os
from .exceptions import *


class AbstractRepository(ABC):

    def __init__(self, db_name):
        self.db_name = db_name

    @abstractmethod
    def save(self, obj):
        pass

    @abstractmethod
    def save_all(self, obj_list):
        pass

    @abstractmethod
    def get_by_id(self, pk):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def delete_by_id(self, pk):
        pass

    @abstractmethod
    def sync(self, obj):
        pass

    @abstractmethod
    def refresh_persistence(self):
        pass


class ShelveRepository(AbstractRepository):
    data_folder = os.path.join(os.path.dirname(__file__), "../data/")

    def __init__(self, db_name: str, sequence_strategy: AbstractSequence.__class__ = IncrementalSequence):
        super().__init__(db_name)
        self.sequence_strategy_cls = sequence_strategy
        self.db = self._open_db()
        self.sequence_strategy = sequence_strategy(self.get_last_id())

    def save(self, obj):
        return self._save(obj)

    def save_all(self, obj_list):
        for obj in obj_list:
            self._save(obj)

    def get_by_id(self, pk):
        if self._id_exists(pk):
            return self._get(pk)
        else:
            raise PersistentObjectDoesNotExists(pk, self.db_name)

    def get_all(self):
        keys = set(self.db.keys())
        objects = []
        for k in keys:
            objects.append(self._get(k))
        return objects

    def delete_by_id(self, pk):
        if self._id_exists(pk):
            self._delete(pk)
        else:
            raise PersistentObjectDoesNotExists(pk, self.db_name)

    def sync(self, obj):
        if self._is_new(obj):
            return None
        else:
            if self._id_exists(obj.pk):
                return self._get(obj.pk)
            else:
                raise PersistentObjectDoesNotExists(obj.pk, self.db_name)

    def refresh_persistence(self):
        self.db.close()
        self.db = self._open_db()

    def _delete(self, pk):
        del self.db[str(pk)]

    def _save(self, obj):
        if self._is_new(obj):
            pk = self.sequence_strategy.next()
            self._set_id(obj, pk)
            self.db[str(pk)] = obj
            return obj
        else:
            self.db[str(obj.pk)] = obj
            return obj

    def _get(self, pk):
        obj = self.db[str(pk)]
        self._set_id(obj, pk)
        return obj

    @staticmethod
    def _is_new(obj):
        return not hasattr(obj, 'pk')

    def _id_exists(self, pk):
        return str(pk) in self.db

    @staticmethod
    def _set_id(obj, pk):
        setattr(obj, 'pk', pk)

    def _open_db(self):
        return shelve.open(self.data_folder + self.db_name, "c")

    def get_last_id(self):
        keys = set(map(int, self.db.keys()))
        if len(keys) == 0:
            return self.sequence_strategy_cls.min_value()
        return max(keys)

    def __del__(self):
        self.db.close()
