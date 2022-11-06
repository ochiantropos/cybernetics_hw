import unittest
from db.sequence import IncrementalSequence


class IncrementalSequenceTest(unittest.TestCase):

    def test_next(self):
        sequence = IncrementalSequence(0)
        self.assertEqual(sequence.next(), 1)
        self.assertEqual(sequence.get_current(), 1)

    def test_see_next(self):
        sequence = IncrementalSequence(10)
        self.assertEqual(sequence.see_next(), 11)
        self.assertEqual(sequence.get_current(), 10)
