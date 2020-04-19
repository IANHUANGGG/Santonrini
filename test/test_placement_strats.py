"""Unit tests for the PlacementStrat Component."""
import unittest
import sys
from santorini.player.place_strat import PlaceStratDiagonal as diag
from santorini.player.place_strat import PlaceStratFar as farthest
from santorini.common.board import Board
from santorini.common.direction import Direction
from santorini.common.worker import Worker


class TestPlaceDiag(unittest.TestCase):
    """Test diagonal placement strategy"""

    def setUp(self):
        self.workers = [Worker("p1", 1),
                        Worker("p1", 2),
                        Worker("p2", 1),
                        Worker("p2", 2)]

    def test_empty(self):
        """Tests placement of four workers on an empty board."""
        board = Board()
        for i in range(len(self.workers)):
            place = diag.get_placement(self.workers[i], board)
            self.assertEqual(place, (i, i))
            board.place_worker(self.workers[i], place)

    def test_call_twice(self):
        """Calling get_placement twice on the same board
        state with different workers."""
        board = Board(workers={self.workers[0]: (0, 0),
                               self.workers[2]: (1, 1)})
        self.assertEqual(diag.get_placement(self.workers[1], board),
                         diag.get_placement(self.workers[3], board))
        self.assertEqual(diag.get_placement(self.workers[1], board),
                         (2, 2))


class TestPlaceFarthest(unittest.TestCase):
    """Test farthest placement strategy"""

    def setUp(self):
        self.workers = [Worker("p1", 1),
                        Worker("p1", 2),
                        Worker("p2", 1),
                        Worker("p2", 2)]

    def test_empty(self):
        """Test placement of two workers on an empty board."""
        board = Board()
        place1 = farthest.get_placement(self.workers[0], board)
        self.assertEqual(place1, (0, 0))

    def test_place_first_worker(self):
        board = Board(workers={self.workers[0]: (0, 0)})
        self.assertEqual(farthest.get_placement(self.workers[2], board),
                         (5, 5))

    def test_two_placed(self):
        """Test placement after p1 places.

        Player 1 has placed two of its workers on the board along the diagonal
        """
        board = Board(workers={self.workers[0]: (0, 0),
                               self.workers[1]: (1, 1)})
        self.assertEqual(farthest.get_placement(self.workers[2], board),
                         (5, 5))

    def test_same_row_placement(self):
        """Test placement after p1 places 2 workers in top row.

        Two workers are placed at (0, 0) and (0, 5) at the top of the board
        and they both belong to the same opposing player
        """
        board = Board(workers={self.workers[0]: (0, 0),
                               self.workers[1]: (0, 5)})
        self.assertEqual(farthest.get_placement(self.workers[2], board),
                         (5, 2))

    def test_two_diag_placement(self):
        """Test placement after p1 places 2 workers in diag row.

        Two workers are placed at (1, 1) and (4, 4) on the diagonal
        and they both belong to the same opposing player
        """
        board = Board(workers={self.workers[0]: (1, 1),
                               self.workers[1]: (4, 4)})
        self.assertEqual(farthest.get_placement(self.workers[2], board),
                         (0, 5))

    def test_far_first(self):
        """Test placement for p2 after p1 places the worker at (0, 5)"""
        board = Board(workers={self.workers[0]: (0, 5)})
        self.assertEqual(farthest.get_placement(self.workers[2], board),
                         (5, 0))

    def test_no_far(self):
        """Test placement of p1 after p1 places the worker at (0, 0)"""
        board = Board(workers={self.workers[0]: (0, 0)})
        self.assertEqual(farthest.get_placement(self.workers[1], board),
                         (0, 1))
