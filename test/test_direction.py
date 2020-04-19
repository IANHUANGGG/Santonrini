"""Unit tests for the Direction Component."""
import unittest
from santorini.common.direction import Direction


class TestDirection(unittest.TestCase):
    """Unit tests for the Direction."""

    def test_move_pos_north(self):
        """Testing moving north."""
        self.assertEqual(Direction.move_position((0, 0), Direction.NORTH),
                         (-1, 0))

    def test_move_pos_south(self):
        """Testing moving south."""
        self.assertEqual(Direction.move_position((0, 0), Direction.SOUTH),
                         (1, 0))

    def test_move_pos_east(self):
        """Testing moving east."""
        self.assertEqual(Direction.move_position((0, 0), Direction.EAST),
                         (0, 1))

    def test_move_pos_west(self):
        """Testing moving west."""
        self.assertEqual(Direction.move_position((0, 0), Direction.WEST),
                         (0, -1))

    def test_move_pos_northeast(self):
        """Testing moving northeast."""
        self.assertEqual(Direction.move_position((0, 0), Direction.NORTHEAST),
                         (-1, 1))

    def test_move_pos_northwest(self):
        """Testing moving northwest."""
        self.assertEqual(Direction.move_position((0, 0), Direction.NORTHWEST),
                         (-1, -1))

    def test_move_pos_southeast(self):
        """Testing moving southeast."""
        self.assertEqual(Direction.move_position((0, 0), Direction.SOUTHEAST),
                         (1, 1))

    def test_move_pos_southwest(self):
        """Testing moving southwest."""
        self.assertEqual(Direction.move_position((0, 0), Direction.SOUTHWEST),
                         (1, -1))

    def test_move_pos_stay(self):
        """Testing not moving."""
        self.assertEqual(Direction.move_position((0, 0), Direction.STAY),
                         (0, 0))

    def test_separate_north(self):
        self.assertEqual(Direction.separate_ew_ns(Direction.NORTH),
                ('PUT','NORTH'))

    def test_separate_south(self):
        self.assertEqual(Direction.separate_ew_ns(Direction.SOUTH),
                ('PUT','SOUTH'))

    def test_separate_east(self):
        self.assertEqual(Direction.separate_ew_ns(Direction.EAST),
                ('EAST','PUT'))

    def test_separate_west(self):
        self.assertEqual(Direction.separate_ew_ns(Direction.WEST),
                ('WEST','PUT'))

    def test_separate_northeast(self):
        self.assertEqual(Direction.separate_ew_ns(Direction.NORTHEAST),
                ('EAST','NORTH'))

    def test_separate_northwest(self):
        self.assertEqual(Direction.separate_ew_ns(Direction.NORTHWEST),
                ('WEST','NORTH'))

    def test_separate_southeast(self):
        self.assertEqual(Direction.separate_ew_ns(Direction.SOUTHEAST),
                ('EAST','SOUTH'))

    def test_separate_southwest(self):
        self.assertEqual(Direction.separate_ew_ns(Direction.SOUTHWEST),
                ('WEST','SOUTH'))
