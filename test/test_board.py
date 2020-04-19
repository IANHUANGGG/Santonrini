"""Unit tests for the Board Component."""
import unittest
from santorini.aux.settings import BOARD_SIZE
from santorini.common.board import Board
from santorini.common.direction import Direction
from santorini.common.worker import Worker


class TestBoard(unittest.TestCase):
    """Board unit tests."""

    def setUp(self):
        """Mock-up context for testing the rulechecker.

        4 workers for 2 players, each placed along the diagonal
        (i.e. (0, 0), (1, 1), etc)
        """
        self.workers = [Worker("player1", 1),
                        Worker("player1", 2),
                        Worker("player2", 1),
                        Worker("player2", 2)]

    def test_place_worker(self):
        """Base case for placing a worker at the start of a game."""
        empty_board = Board()
        empty_board.place_worker(self.workers[0], (0, 0))
        self.assertEqual(empty_board.worker_position(self.workers[0]), (0, 0))

    def test_workers(self):
        board = Board()
        self.assertTrue(board.workers == [])

    def test_assert_bounds(self):
        board = Board()
        with self.assertRaises(IndexError):
            board.assert_bounds((-1,-1))

    def test_place_worker_off_board(self):
        """Case for placing a worker outside of the board boundaries."""
        empty_board = Board()

        with self.assertRaises(IndexError) as context:
            empty_board.place_worker(self.workers[0], (-1, -1))
        self.assertTrue("Cannot place a worker out of board bounds" in
                        str(context.exception))

    def test_place_more_than_4_workers(self):
        """Case for placing more than 4 workers."""
        board = Board([[0, 1, 2, 3, 4, 0]],
                      {self.workers[0]: (0, 0),
                       self.workers[1]: (0, 1),
                       self.workers[2]: (0, 2),
                       self.workers[3]: (0, 3)})

        self.assertEqual(len(board.workers), 4)
        board.place_worker(Worker("player3", 2), (0, 5))
        self.assertEqual(len(board.workers), 5)

    def test_place_worker_on_worker(self):
        """Case for placing a worker onto another worker."""
        empty_board = Board()
        empty_board.place_worker(self.workers[0], (0, 0))
        self.assertEqual(empty_board.worker_position(self.workers[1]), None)
        empty_board.place_worker(self.workers[1], (0, 0))
        self.assertEqual(empty_board.worker_position(self.workers[0]),
                         empty_board.worker_position(self.workers[1]))

    def test_move_worker(self):
        """Base case for moving a worker."""
        board = Board([[0, 1]],
                      {self.workers[0]: (0, 0)})
        self.assertEqual(board.worker_position(self.workers[0]), (0, 0))
        board.move_worker(self.workers[0], Direction.EAST)
        self.assertEqual(board.worker_position(self.workers[0]), (0, 1))
        board.move_worker(self.workers[0], Direction.SOUTH)
        self.assertEqual(board.worker_position(self.workers[0]), (1, 1))
        board.move_worker(self.workers[0], Direction.WEST)
        self.assertEqual(board.worker_position(self.workers[0]), (1, 0))
        board.move_worker(self.workers[0], Direction.NORTH)
        self.assertEqual(board.worker_position(self.workers[0]), (0, 0))

    def test_move_worker_off_board(self):
        """Case for moving a worker outside of the board boundaries."""
        board = Board([[0, 1]],
                      {self.workers[0]: (0, 0)})

        self.assertEqual(board.worker_position(self.workers[0]), (0, 0))
        with self.assertRaises(IndexError) as context:
            board.move_worker(self.workers[0], Direction.NORTH)
        self.assertTrue("Cannot place a worker out of board bounds" in
                        str(context.exception))

    def test_move_worker_on_worker(self):
        """Case for moving a worker onto another worker."""
        board = Board([[0, 1]],
                      {self.workers[0]: (0, 0),
                       self.workers[1]: (1, 1)})

        self.assertEqual(board.worker_position(self.workers[0]), (0, 0))
        self.assertEqual(board.worker_position(self.workers[1]), (1, 1))
        self.assertTrue(board.is_occupied(
                        board.worker_position(self.workers[1])))
        board.move_worker(self.workers[0], Direction.SOUTHEAST)
        self.assertEqual(board.worker_position(self.workers[0]),
                         board.worker_position(self.workers[1]))

    def test_move_worker_onto_building(self):
        """Case for moving a worker onto a building.

        In this case, the building is 1 floor higher than the current worker
        """
        board = Board([[0, 1]],
                      {self.workers[0]: (0, 0)})
        self.assertEqual(board.worker_position(self.workers[0]), (0, 0))
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.STAY),
                         0)
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.EAST),
                         1)
        board.move_worker(self.workers[0], Direction.EAST)
        self.assertEqual(board.worker_position(self.workers[0]),
                         (0, 1))
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.STAY),
                         1)

    def test_move_worker_onto_high_building(self):
        """Case for moving a worker onto a high building.

        In this case, the building is 2 or more floors higher than the current
        worker
        """
        board = Board([[0, 2]],
                      {self.workers[0]: (0, 0)})
        self.assertEqual(board.worker_position(self.workers[0]), (0, 0))
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.STAY),
                         0)
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.EAST),
                         2)
        board.move_worker(self.workers[0], Direction.EAST)
        self.assertEqual(board.worker_position(self.workers[0]), (0, 1))
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.STAY),
                         2)

    def test_build_floor(self):
        """Base case for building a floor onto a building.

        We create a custom board and place two workers on it, and
        test building floors at different levels & from
        different positions on the same cell.
        """
        board = Board([[0, 1, 2, 3, 4, 0]],
                      {self.workers[0]: (0, 0),
                       self.workers[1]: (0, 2)})
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.EAST),
                         1)
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[1]),
                         Direction.WEST),
                         1)
        board.build_floor(self.workers[0], Direction.EAST)
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.EAST),
                         2)
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[1]),
                         Direction.WEST),
                         2)
        board.build_floor(self.workers[1], Direction.WEST)
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[1]),
                         Direction.WEST),
                         3)

    def test_build_floor_off_board(self):
        """Case for building a floor off of the board."""
        board = Board([[0, 2]],
                      {self.workers[0]: (0, 0)})
        with self.assertRaises(IndexError) as context:
            board.build_floor(self.workers[0], Direction.NORTH)
        self.assertTrue("Cannot place a worker out of board bounds" in
                        str(context.exception))

    def test_build_floor_on_worker(self):
        """Case for building a floor on top of another worker."""
        board = Board(workers={self.workers[0]: (0, 0),
                               self.workers[1]: (1, 1)})
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.SOUTHEAST), 0)
        board.build_floor(self.workers[0], Direction.SOUTHEAST)
        self.assertTrue(board.is_occupied((1, 1)))
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.SOUTHEAST), 1)

    def test_build_floor_above_max(self):
        """Case for building a floor onto a building already at MAX_HEIGHT."""
        board = Board([[0, 4]],
                      {self.workers[0]: (0, 0)})
        with self.assertRaises(OverflowError) as context:
            board.build_floor(self.workers[0], Direction.EAST)
        self.assertTrue("Cannot build over" in
                        str(context.exception))

    def test_get_height(self):
        """Base case for getting the height of a building."""
        board = Board([[0, 3]],
                      {self.workers[0]: (0, 0)})
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.EAST),
                         3)
        self.assertEqual(board.get_height(
                         board.worker_position(self.workers[0]),
                         Direction.STAY),
                         0)

    def test_get_height_off_board(self):
        """Case for getting the height of a building off of the board."""
        board = Board([[0, 3]],
                      {self.workers[0]: (0, 0)})
        with self.assertRaises(IndexError) as context:
            board.get_height(board.worker_position(self.workers[0]),
                             Direction.NORTH)
        self.assertTrue("Cannot place a worker out of board bounds" in
                        str(context.exception))

    def test_is_maxheight(self):
        """Base case for seeing if a building is at MAX_HEIGHT."""
        board = Board([[0, 4]],
                      {self.workers[0]: (0, 0)})
        self.assertTrue(board.is_maxheight(
                        board.worker_position(self.workers[0]),
                        Direction.EAST))

    def test_is_not_maxheight(self):
        """Case for seeing if a building isn't at MAX_HEIGHT."""
        board = Board([[0, 4]],
                      {self.workers[0]: (0, 0)})
        self.assertFalse(board.is_maxheight(
                         board.worker_position(self.workers[0]),
                         Direction.STAY))

    def test_is_occupied(self):
        """Base case for seeing if a cell is occupied by a worker."""
        board = Board([[0, 4]],
                      {self.workers[0]: (0, 0)})
        self.assertEqual(board.worker_position(self.workers[0]), (0, 0))
        self.assertTrue(board.is_occupied((0, 0)))

    def test_is_not_occupied(self):
        """Case for seeing if a cell is not occupied by a worker."""
        board = Board([[0, 4]],
                      {self.workers[0]: (0, 0),
                       self.workers[1]: (1, 1)})
        self.assertEqual(board.worker_position(self.workers[1]), (1, 1))
        self.assertFalse(board.is_occupied((1, 2)))

    def test_is_neighbor(self):
        """Base case for seeing if a worker has a neighboring cell."""
        board = Board(workers={self.workers[0]: (0, 0)})
        self.assertTrue(board.is_neighbor(self.workers[0],
                                          Direction.EAST))
        self.assertTrue(board.is_neighbor(self.workers[0],
                                          Direction.SOUTHEAST))
        self.assertTrue(board.is_neighbor(self.workers[0],
                                          Direction.SOUTH))
        self.assertTrue(board.is_neighbor(self.workers[0],
                                          Direction.STAY))

    def test_is_not_neighbor(self):
        """Case for seeing if a worker doesn't have a neighboring cell."""
        board = Board(workers={self.workers[0]: (0, 0)})
        self.assertFalse(board.is_neighbor(self.workers[0],
                                           Direction.NORTH))
        self.assertFalse(board.is_neighbor(self.workers[0],
                                           Direction.NORTHEAST))
        self.assertFalse(board.is_neighbor(self.workers[0],
                                           Direction.WEST))
        self.assertFalse(board.is_neighbor(self.workers[0],
                                           Direction.NORTHWEST))
        self.assertFalse(board.is_neighbor(self.workers[0],
                                           Direction.SOUTHWEST))

    def test_building_is_max_height(self):
        """Test on the building to see if it is at max height."""
        board = Board([[4]], workers={self.workers[0]: (1, 0)})
        self.assertTrue(board.is_maxheight(
                        board.worker_position(self.workers[0]),
                        Direction.NORTH))

    def test_building_is_not_max_height(self):
        """Test on the building to see if it is at max height."""
        board = Board([[3]], workers={self.workers[0]: (1, 0)})
        self.assertFalse(board.is_maxheight(
                         board.worker_position(self.workers[0]),
                         Direction.NORTH))

    def test_board_into_list(self):
        """Test board_into_list() returns a list of 0s for an empty board"""
        board = Board()
        board_list = board.board_into_list()
        expected = [[0] * BOARD_SIZE for row in range(BOARD_SIZE)]
        self.assertEqual(board_list, expected)

