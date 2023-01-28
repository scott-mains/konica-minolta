import unittest
from api.utils import is_horizontal, is_vertical, is_diagonal, is_octilinear


class TestUtils(unittest.TestCase):

    def test_is_horizontal(self):
        for direction in (
            1,
            2,
            45,
            90,
            135,
        ):
            self.assertFalse(is_horizontal(direction))

        for direction in (
            0,
            180,
            -180,
        ):
            self.assertTrue(is_horizontal(direction))

    def test_is_vertical(self):
        pass

    def test_is_diagonal(self):
        pass

    def test_is_octilinear(self):
        pass


if __name__ == '__main__':
    unittest.main()
