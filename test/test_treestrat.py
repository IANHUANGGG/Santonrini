"""Unit tests for the Strat Component."""
import unittest
import copy
from santorini.player.place_strat import PlaceStratDiagonal, PlaceStratFar
from santorini.player.tree_strat import TreeStrategy as tree
from santorini.player.strategy import Strategy
from santorini.common.board import Board
from santorini.common.direction import Direction
from santorini.common.worker import Worker

class TestStrategy(unittest.TestCase):
    """Test farthest placement strategy."""

    def setUp(self):
        self.workers = [Worker("p1", 1),
                        Worker("p1", 2),
                        Worker("p2", 1),
                        Worker("p2", 2)]

        self.place_dia = PlaceStratDiagonal()
        self.place_far = PlaceStratFar()


    # def test_get_turn(self):
    #     """Test that get_turn returns the correct turn
    #     for a simple test case."""
    #     board = Board([[2, 3]],
    #                   workers={self.workers[i]: (i, i)
    #                            for i in range(len(self.workers))})
    #     tree_strat = tree(2)
        #self.assertEqual(tree_strat.get_turn(self.workers[0:2], board),
        #                (self.workers[0], Direction.SOUTH, Direction.NORTH))

    # def test_get_turn_forced(self):
    #     """Test that get_turn returns the correct turn
    #     for a simple test case."""
    #     board = Board([[2, 3],
    #                    [4, 0]],
    #                   workers={self.workers[i]: (i, i)
    #                            for i in range(len(self.workers))})
    #     tree_strat = tree(2)
        #self.assertEqual(tree_strat.get_turn(self.workers[0:2], board),
        #                (self.workers[0], Direction.EAST, Direction.SOUTHEAST))

    # def test_depth_zero(self):
    #     """Test tree strategy for a depth of zero."""
    #     board = Board([[2, 3]],
    #                   workers={self.workers[i]: (i, i)
    #                            for i in range(len(self.workers))})
    #     self.assertTrue(tree.do_survive(board, 0, False, "p1", "p2", self.workers[0],
    #                                     Direction.EAST))
    #     self.assertTrue(tree.do_survive(board, 0, False, "p1", "p2", self.workers[0],
    #                                     Direction.SOUTH, Direction.NORTH))

    def test_depth_one_and_two(self):
        """Test tree strategy for a depth of one."""
        board = Board([[2, 3], [2, 2, 2, 2]],
                      workers={self.workers[i]: (1, i)
                               for i in range(len(self.workers))})
        # self.assertTrue(tree.do_survive(board, 1, False, "p1", "p2", self.workers[1],
        #                                 Direction.NORTH))
        # self.assertTrue(tree.do_survive(board, 1, False, "p1", "p2", self.workers[0],
        #                                 Direction.NORTH, Direction.EAST))
        # self.assertTrue(tree.do_survive(board, 1, False, "p1", "p2", self.workers[0],
        #                                  Direction.SOUTH, Direction.EAST))
        # self.assertTrue(tree.do_survive(board, 1, False, "p1", "p2",self.workers[1],
        #                                  Direction.SOUTH, Direction.EAST))
        # self.assertFalse(tree.do_survive(board, 2, False, "p1", "p2",self.workers[1],
        #                                  Direction.SOUTH, Direction.EAST))
    def test_survive_atmost_4_rounds(self):
        board_d4 = Board([[0,4,0,0,4,0], [4,0,4,0,4,4], [4], [0], [0,2,0,0,4,4], [1,0,3,0,4,2]],
                        workers = {self.workers[0]: (0,0), self.workers[1]:(5,5),
                                    self.workers[2]: (5,0), self.workers[3]:(0,5)})
        # should be able to survive for 2 rounds
        # print(board_d4)
        # self.assertTrue(tree.do_survive(board_d4, 2, False, "p1", "p2", self.workers[0],
        #                                 Direction.SOUTHEAST, Direction.EAST))
        # # Should NOT be able to survive for 4 rounds
        # self.assertTrue(tree.do_survive(board_d4, 3, False, "p1", "p2", self.workers[0],
        #                                 Direction.SOUTHEAST, Direction.EAST))
        self.assertFalse(tree.do_survive(board_d4, 4, False, "p1", "p2", self.workers[0],
                                        Direction.SOUTHEAST, Direction.SOUTH))

    # def test_survive_atmost_3_rounds(self):
    #     board_d3 = Board([[1,2,3,0,4,0], [0,0,0,0,4,4],[0],[0],[0,0,0,0,4,4],[0,0,0,0,4,0]], 
    #                 workers = {self.workers[0]:(0,0), self.workers[1]:(0,5),
    #                             self.workers[2]: (5,5), self.workers[3]: (5,0)})
    #     # self.assertTrue(tree.do_survive(board_d3, 2, False, "p1", "p2", self.workers[0],
    #     #                                 Direction.EAST, Direction.SOUTH))
    #     self.assertFalse(tree.do_survive(board_d3, 3, False, "p1", "p2", self.workers[0],
    #                                     Direction.EAST, Direction.SOUTH))


    # def test_depth_one_again(self):
    #     """Test tree strategy for a depth of one again."""
    #     board = Board([[2, 3],
    #                    [2, 2, 2, 2],
    #                    [0, 1, 3, 2, 3, 1],
    #                    [0, 3, 2, 1, 2, 3]],
    #                   workers={self.workers[i]: (1, i)
    #                            for i in range(len(self.workers))})
    #     # self.assertTrue(tree.do_survive(board, "p1", 1, self.workers[1],
    #     #                                 Direction.SOUTHEAST))
    #     self.assertFalse(tree.do_survive(board, 1, False, "p1", "p2", self.workers[0],
    #                                      Direction.SOUTH, Direction.EAST))
    #     self.assertTrue(tree.do_survive(board, 1, False self.workers[2],
    #                                     Direction.SOUTH))

    # def test_depth_two_example(self):
    #     """Test tree strategy for a depth of two.

    #     This is specifically the test Matthias posts on the project page.
    #     """
    #     board = Board([[0, 1, 3, 2],
    #                    [0, 2, 3]],
    #                   workers={self.workers[0]: (0, 0),
    #                            self.workers[1]: (0, 1),
    #                            self.workers[2]: (0, 2),
    #                            self.workers[3]: (1, 1)})
    #     self.assertFalse(tree.do_survive(board, 2, False, "p1",
    #                                      "p2", self.workers[1],
    #                                      Direction.SOUTHWEST,
    #                                      Direction.SOUTH))

    # def test_depth_three_example(self):
    #     """Test tree strategy for a depth of three.

    #     This is specifically the test Matthias posts on the project page.
    #     """
    #     board = Board([[0, 0],
    #                    [3, 0]],
    #                   workers={self.workers[0]: (0, 0),
    #                            self.workers[1]: (0, 1),
    #                            self.workers[2]: (2, 0),
    #                            self.workers[3]: (2, 1)})
    #     self.assertTrue(tree.do_survive(board, 3, False, "p1",
    #                                     "p2", self.workers[0],
    #                                     Direction.SOUTHEAST,
    #                                     Direction.WEST))

    # def test_depth2_boxin(self):
    #     """Test tree strategy for a depth of 2 on boxin config."""
    #     board = Board([[0, 0, 1, 0],
    #                    [0, 4, 4],
    #                    [4, 4]],
    #                   workers={self.workers[0]: (0, 0),
    #                            self.workers[1]: (0, 1),
    #                            self.workers[2]: (0, 2),
    #                            self.workers[3]: (0, 3)})
    #     self.assertFalse(tree.do_survive(board, 2, False, 
    #                                      "p1", "p2", self.workers[1],
    #                                      Direction.SOUTHWEST,
    #                                      Direction.NORTHEAST))

    # def test_depth1_boxin(self):
    #     """Test tree strategy for a depth of 2 on boxin config."""
    #     board = Board([[0, 0, 1, 0],
    #                    [0, 4, 4],
    #                    [4, 4]],
    #                   workers={self.workers[0]: (0, 0),
    #                            self.workers[1]: (0, 1),
    #                            self.workers[2]: (0, 2),
    #                            self.workers[3]: (0, 3)})
    #     tree1 = tree()
    #     self.assertTrue(tree1.do_survive(board, 1,
    #                                      False, "p1", "p2", self.workers[1],
    #                                      Direction.SOUTHWEST,
    #                                      Direction.NORTHEAST))

    # def test_depth4(self):
    #     """Test tree strategy for a depth of 4."""
    #     board = Board(workers={self.workers[0]: (0, 0),
    #                            self.workers[1]: (1, 1),
    #                            self.workers[2]: (2, 2),
    #                            self.workers[3]: (3, 3)})
    #     self.assertTrue(tree.do_survive(board, 4, False, 
    #                                     "p1", "p2", self.workers[0]))
