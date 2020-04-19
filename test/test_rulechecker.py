"""Unit tests for the Rulechecker Component."""
import unittest
import copy
from santorini.common.rulechecker import RuleChecker
from santorini.common.board import Board
from santorini.common.direction import Direction
from santorini.common.worker import Worker

class TestRulechecker(unittest.TestCase):
    """Rulechecker test Class."""

    def setUp(self):
        """Mock-up context for testing the self.rulechecker.

        4 workers for 2 players, each placed along the diagonal
        (i.e. (0, 0), (1, 1), etc)

        To the east of each worker, a building is built with
        height equal to the worker's number in the total
        workers (i.e. Worker 2 builds a 2-floor building)

        Example:
        0W | 1  | 0  | 0  | 0 | 0
        0  | 0W | 2  | 0  | 0 | 0
        0  | 0  | 0W | 3  | 0 | 0
        0  | 0  | 0  | 0W | 4 | 0
        0  | 0  | 0  | 0  | 0 | 0
        0  | 0  | 0  | 0  | 0 | 0

        """
        self.workers = [Worker("player1", 1),
                        Worker("player1", 2),
                        Worker("player2", 1),
                        Worker("player2", 2)]
        self.board = Board()
        for i, worker in enumerate(self.workers):
            self.board.place_worker(worker, (i, i))
            for _ in range(i):
                self.board.build_floor(worker, Direction.EAST)

        self.rulechecker = RuleChecker()

    def test_can_move_offboard(self):
        """Case for testing if you can move to a position off the board.

        * Worker at position (0,0) wants to move to the north
        * Worker at position (0,0) wants to move to the northwest
        * Worker at position (0,0) wants to move to the west
        * Worker at position (0,0) wants to move to the southwest
        """
        self.assertFalse(self.rulechecker.can_move_build(self.board,"player1",
                                                    self.workers[0],
                                                    Direction.NORTH))
        self.assertFalse(self.rulechecker.can_move_build(self.board,"player1",
                                                    self.workers[0],
                                                    Direction.NORTHWEST))
        self.assertFalse(self.rulechecker.can_move_build(self.board,"player1",
                                                    self.workers[0],
                                                    Direction.WEST))
        self.assertFalse(self.rulechecker.can_move_build(self.board,"player1",
                                                    self.workers[0],
                                                    Direction.SOUTHWEST))

    def test_can_move_onto_worker(self):
        """Testing if you can move to a position occupied by another worker.

        * Worker at position (0,0) wants to move to the Worker on
        position (1, 1)
        """
        self.assertFalse(self.rulechecker.can_move_build(self.board,"player1",
                                                    self.workers[1],
                                                    Direction.SOUTHEAST))

    def test_can_move_high_building(self):
        """Testing that you cannot move two floors higher than current pos.

        * Worker at position (2,2) with height 0 wants to move to east
        to a building with height 2
        """
        self.assertFalse(self.rulechecker.can_move_build(self.board,"player2",
                                                    self.workers[2],
                                                    Direction.EAST))

    def test_can_move_down_2_floors(self):
        """Case for testing if you can move from two floors down.

        * Worker at position (2,2) wants to move to the north,
        which has a building with height 1
        * Worker at position (1,2) wants to move to the southwest,
        which has a building of height 2
        * Worker at position (2,3) wants to move to the west,
        which has no building (i.e height 0)
        """
        board_copy = copy.copy(self.board)
        board_copy.move_worker(self.workers[1], Direction.NORTH)
        board_copy.move_worker(self.workers[1], Direction.SOUTHEAST)
        self.assertTrue(self.rulechecker.can_move_build(board_copy,"player2",
                                                   self.workers[2],
                                                   Direction.WEST,
                                                   Direction.SOUTH))

    def test_can_no_move(self):
        """Case for testing if you can not have a movement."""
        self.assertFalse(self.rulechecker.can_move_build(self.board,"player1",
                                                    self.workers[0],
                                                    Direction.STAY))

    def test_can_build(self):
        """Base case for can_build."""
        self.assertTrue(self.rulechecker.can_move_build(self.board,"player1",
                                                   self.workers[0],
                                                   Direction.EAST,
                                                   Direction.EAST))

    def test_can_build_off_board(self):
        """Case for building off of the board."""
        self.assertFalse(self.rulechecker.can_move_build(self.board,"player1",
                                                    self.workers[0],
                                                    Direction.EAST,
                                                    Direction.NORTH))

    def test_can_build_another_worker(self):
        """Case for building onto a position that contains another worker."""
        self.assertFalse(self.rulechecker.can_move_build(self.board,"player1",
                                                    self.workers[1],
                                                    Direction.EAST,
                                                    Direction.SOUTH))

    def test_can_build_at_max_height(self):
        """Case for building onto a building that is already MAX_HEIGHT(4)."""
        board_copy = copy.copy(self.board)
        board_copy.build_floor(self.workers[3], Direction.EAST)
        self.assertFalse(self.rulechecker.can_move_build(board_copy,"player2",
                                                    self.workers[3],
                                                    Direction.NORTHEAST,
                                                    Direction.SOUTH))

    def test_can_build_no_move(self):
        """Case for building a building on the worker location."""
        board_copy = copy.copy(self.board)
        self.assertFalse(self.rulechecker.can_move_build(board_copy,"player2",
                                                    self.workers[2],
                                                    Direction.WEST,
                                                    Direction.STAY))

    def test_can_place_worker(self):
        """Base case for placing a worker at the start of a game."""
        board = Board()
        self.assertTrue(self.rulechecker.can_place_worker(board, "player1", self.workers[0],
                                                     (0, 0)))

    def test_can_place_worker_twice(self):
        """Base case for placing a worker at the start of a game."""
        board = Board()
        self.assertTrue(self.rulechecker.can_place_worker(board, "player1", self.workers[0],
                                                     (0, 0)))
        board.place_worker(self.workers[0], (0, 0))
        self.assertFalse(self.rulechecker.can_place_worker(board, "player1", self.workers[0],
                                                      (0, 0)))
        self.assertFalse(self.rulechecker.can_place_worker(board, "player1", self.workers[0],
                                                      (4, 4)))

    def test_can_place_worker_off_board(self):
        """Case for placing a worker outside of the board boundaries."""
        board = Board()
        self.assertFalse(self.rulechecker.can_place_worker(board, "player1", self.workers[0],
                                                      (-1, -1)))

    def test_can_place_five_workers(self):
        """Case for placing more than 4 workers."""
        board = Board([[0, 1, 2, 3, 4, 0]],
                      {self.workers[0]: (0, 0),
                       self.workers[1]: (0, 1),
                       self.workers[2]: (0, 2),
                       self.workers[3]: (0, 3)})
        self.assertFalse(self.rulechecker.can_place_worker(board, "player3",
                                                      Worker("player3", 2),
                                                      (0, 5)))

    def test_can_place_worker_on_worker(self):
        """Case for placing a worker onto another worker."""
        board = Board(workers={self.workers[0]: (0, 0),
                               self.workers[1]: (0, 1),
                               self.workers[2]: (0, 2)})
        self.assertFalse(self.rulechecker.can_place_worker(board, "player2",
                                                      Worker("player2", 2),
                                                      (0, 1)))

    def test_is_game_over_height_three(self):
        """A worker is on a building of height 3."""
        board = Board([[3]], workers={self.workers[0]: (0, 0),
                                      self.workers[1]: (0, 1),
                                      self.workers[2]: (0, 2)})
        #self.assertTrue(self.rulechecker.is_game_over(board, self.workers[0:2]))
        self.assertTrue(self.rulechecker.is_game_over(board, 'player1'))

    def test_is_game_over_goto_h_three(self):
        """Testing game over case.

        a worker is on a building of height 2,
        builds a floor, and moves to a building of
        height 3
        """
        board = Board([[2, 0, 0, 0, 0, 0],
                       [2, 2, 0, 0, 0, 0]],
                      workers={self.workers[0]: (1, 0),
                               self.workers[1]: (1, 1)})
        #self.assertFalse(self.rulechecker.is_game_over(board, self.workers[0:2]))
        self.assertFalse(self.rulechecker.is_game_over(board, 'player1'))
        board.build_floor(self.workers[0], Direction.NORTH)
        board.move_worker(self.workers[0], Direction.NORTH)
        #self.assertTrue(self.rulechecker.is_game_over(board, self.workers[0:2]))
        self.assertTrue(self.rulechecker.is_game_over(board, 'player1'))

    def test_is_game_over_can_move(self):
        """Testing game over case.

        A worker can move
        """
        board = Board([[2, 2, 0, 0, 0, 0],
                       [4, 4, 0, 0, 0, 0]],
                      workers={self.workers[0]: (0, 0),
                               self.workers[1]: (0, 1),
                               self.workers[2]: (0, 5),
                               self.workers[3]: (1, 4)})
        #self.assertFalse(self.rulechecker.is_game_over(board, self.workers[0:2]))
        self.assertFalse(self.rulechecker.is_game_over(board, 'player1'))

    def test_is_game_over_can_build(self):
        """Testing game over case.

        a worker is on a building of height 0 and has
        no valid move, but has a valid build
        """
        board = Board([[0, 3, 0, 0, 0, 0],
                       [4, 4, 0, 0, 0, 0]],
                      workers={self.workers[0]: (0, 0),
                               self.workers[1]: (0, 1),
                               self.workers[2]: (0, 5),
                               self.workers[3]: (1, 4)})
        #self.assertTrue(self.rulechecker.is_game_over(board, self.workers[0:2]))
        self.assertTrue(self.rulechecker.is_game_over(board, 'player1'))

    def test_can_move_build_on_same_pos(self):
        """Check that a Worker can build on the spot they just moved from."""
        board = Board(workers={self.workers[0]: (0, 0)})
        self.assertTrue(self.rulechecker.can_move_build(board, "player1", self.workers[0],
                                                   Direction.SOUTH,
                                                   Direction.NORTH))
    
    def test_winner_1(self):
        """Get the winner."""
        board = Board([[0,0,3,0,0,0]], workers={self.workers[0]: (0, 2)})
        self.assertEqual(self.rulechecker.get_winner(board), "player1")
    
    def test_no_winner(self):
        """Get the winner."""
        board = Board(workers={self.workers[0]: (0, 2)})
        self.assertFalse(self.rulechecker.get_winner(board))
    
    def test_winner_2(self):
        """Get the winner."""
        board = Board([[1,2,3,4,3,2]], workers={self.workers[0]: (0, 0), self.workers[2]: (0, 1)})
        self.assertFalse(self.rulechecker.get_winner(board))
        board.move_worker(self.workers[2], Direction.EAST)
        self.assertEqual(self.rulechecker.get_winner(board), "player2")
    
    def test_winner_lock_in(self):
        board = Board([[0, 1, 3, 4, 3, 0],
                       [1, 2, 4, 4, 4, 3]], 
                      workers={self.workers[0]: (0, 0), self.workers[1]: (0, 5), 
                                self.workers[2]: (1, 0), self.workers[3]: (0, 1)})
        self.assertEqual(self.rulechecker.get_winner(board), "player2")

    def test_winner_move_no_build(self):
        board = Board([[0, 0, 1, 0],
                      [0, 4, 4],
                      [4, 4]],
                      workers={self.workers[0]: (0, 0),
                               self.workers[1]: (1, 0),
                               self.workers[2]: (0, 1),
                               self.workers[3]: (0, 3)})
        self.assertEqual(self.rulechecker.get_winner(board), "player2")