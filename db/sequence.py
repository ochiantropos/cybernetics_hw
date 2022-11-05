from abc import ABC, abstractmethod


class AbstractSequence(ABC):

    def __init__(self, last_id):
        self.last_id = last_id

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def see_next(self):
        pass

    @staticmethod
    def min_value():
        pass

    def get_current(self):
        return self.last_id


class IncrementalSequenceStrategy(AbstractSequence):

    def next(self):
        self.last_id += 1
        return self.last_id

    def see_next(self):
        return self.last_id + 1

    @staticmethod
    def min_value():
        return 0
