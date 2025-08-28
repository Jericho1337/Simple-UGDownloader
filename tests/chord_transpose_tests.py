import unittest

from src import ChordTransposer

class TestChordTranspose(unittest.TestCase):

    def chord_transpose(self):
        self.assertEqual(ChordTransposer.ChordTransposer.chord_transposer("Am", 2), "Bm", "Should be Bm (Am+2)")

if __name__ == "__main__":
    unittest.main()