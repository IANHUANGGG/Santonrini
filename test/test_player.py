import unittest
from santorini.admin.referee import Referee
from santorini.common.board import Board
from santorini.common.worker import Worker
from santorini.common.rulechecker import RuleChecker
from santorini.player.player import Player
from santorini.player.place_strat import PlaceStratDiagonal
from santorini.player.tree_strat import TreeStrategy
from santorini.player.strategy import Strategy

class TestPlayer(unittest.TestCase):

    def setUp(self):
        pl_strat = PlaceStratDiagonal()
        tree = TreeStrategy()
        strategy = Strategy(pl_strat, tree)
        self.player1 = Player('pl',strategy)
        self.player2 = Player('p2',strategy)

    def test_place_worker(self):
        board = Board()
        referee = Referee(board, self.player1, self.player2)
        rules = RuleChecker()
        referee.worker_placement(rules)
        self.assertTrue(len(board._workers) == 4)

    def test_play_turn(self):
        board = Board()
        referee = Referee(board, self.player1, self.player2)
        rules = RuleChecker()
        referee.worker_placement(rules)
        referee.execute_turn(self.player1,1,rules)
        levels = [[building.floor > 0 for building in row] for row in board._board]
        self.assertTrue(any(any(row) for row in levels))

'''
    def test_game_over(self):
        board = Board()
        referee = Referee(board, self.player1, self.player2)
        rules = RuleChecker()
        referee.worker_placement(rules)
        #############3
        print('player_worker_game_over',board.workers)
        ############
        self.assertTrue(len(board.workers) == 4)
        self.player1.game_over(self.player1)
        self.player2.game_over(self.player2)
        #############3
        print('AFTER GAME OVER:',board.players)
        ############
        self.assertTrue(len(board.workers) == 0)
'''
        
        

