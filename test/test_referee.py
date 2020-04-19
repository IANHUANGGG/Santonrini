import unittest
import copy
from contextlib import contextmanager
from io import StringIO
import sys
from santorini.admin.referee import Referee
from santorini.common.board import Board
from santorini.common.rulechecker import RuleChecker
from santorini.observer.observer import Observer
from santorini.observer.action import Action
from santorini.player.breaking_player import BreakingPlayer
from santorini.player.player import Player
from santorini.player.place_strat import PlaceStratDiagonal, PlaceStratFar
from santorini.player.strategy import Strategy
from santorini.player.tree_strat import TreeStrategy

class TestReferee(unittest.TestCase):
    """Tests for the Referee component."""

    def setUp(self):
        """ Mock-up context to test the Referee component.

        2 different players and 1 board.

        """
        placement_strat = PlaceStratFar()
        tree_strat = TreeStrategy(1)
        self.strategy = Strategy(placement_strat,tree_strat)

        self.board = Board()
        self.player1 = Player('ian',self.strategy)
        self.player2 = Player('hyeonjung',self.strategy)

        self.rulechecker = RuleChecker()

        self.referee = Referee(Board(), self.player1, self.player2)
        
    def RuleBreaker(self, badplayer):
        normal_player = Player("normal", self.strategy)
        new_referee = Referee(Board(), badplayer, normal_player)
        new_referee.worker_placement(self.rulechecker)
        return new_referee.winner

    def test_worker_placement(self):
        self.referee.worker_placement(self.rulechecker)
        self.assertTrue(len(self.referee.board._workers) == 4)
        
    def test_worker_placement_timeout(self):
        player_never_return = TestReferee.PlayerNeverReturn("abc", self.strategy)
        self.assertTrue(self.RuleBreaker(player_never_return), "normal")

    def test_worker_placement_placement_invalid_format(self):
        player_return_nonsense = TestReferee.ReturnNonsense("abc", self.strategy)
        self.assertTrue(self.RuleBreaker(player_return_nonsense), "normal")

    def test_initialize_referee_w_same_named_players(self):
        p1 = Player

    def test_execute_turn(self):
        self.referee.worker_placement(self.rulechecker)
        self.referee.execute_turn(self.player1, 1, self.rulechecker)
        self.assertTrue(any(self.board._board))

    def test_run_game(self):
        winner = self.referee.run_game(self.rulechecker)
        self.assertTrue(self.referee.winner == 'ian' or self.referee.winner ==
        'hyeonjung')

    def test_best_of(self):
        winner = self.referee.best_of(2,self.rulechecker)[0]
        self.assertTrue(self.referee.winner == 'ian' 
                or self.referee.winner == 'hyeonjung')

    def test_best_of_misbehaver(self):
        p1 = Player('p1',self.strategy)
        p2 = Player('p2',self.strategy)
        referee = Referee(Board(),p1,p2)
        rules = RuleChecker()
        referee.misbehaver = 'p1'
        referee.best_of(1,rules)
        board = referee.board._board
        levels = [[building.floor > 0 for building in row] for row in board]
        self.assertFalse(any(any(row) for row in levels))


    def test_best_of_has_winner_with_even_number_of_rounds(self):
        winner = self.referee.best_of(2, self.rulechecker)[0]
        self.assertTrue(self.referee.winner != None)
        self.assertTrue(winner == 'ian' or winner == 'hyeonjung')

    def test_steady_state(self):
        p1 = Player('p1',self.strategy)
        p2 = Player('p2',self.strategy)
        referee = Referee(Board(),p1,p2)
        rules = RuleChecker()
        referee.worker_placement(rules)
        referee.steady_state(rules)
        self.assertTrue(referee.winner == 'p1' 
                or referee.winner == 'p2')

    def test_execute_turn2(self):
        p1 = Player('p1',self.strategy)
        p2 = Player('p2',self.strategy)
        referee = Referee(Board(),p1,p2)
        rules = RuleChecker()
        referee.worker_placement(rules)
        board = referee.board.board_into_list()
        referee.execute_turn(p1,1,rules)
        board2 = referee.board.board_into_list()
        self.assertTrue(board != board2)

    def test_execute_turn_misbehavior(self):
        broken = BreakingPlayer('broken')
        p1 = Player('p1',self.strategy)
        referee = Referee(Board(),broken,p1)
        rules = RuleChecker()
        referee.worker_placement(rules)
        referee.execute_turn(broken,1,rules)
        self.assertTrue(referee.misbehaver == 'broken')
        self.assertTrue(referee.winner == 'p1')

    def test_same_player(self):
        with self.assertRaises(ValueError):
            Referee(Board(), self.player1, self.player1)

    def test_add_observer(self):
        referee = Referee(Board(), self.player1, self.player2)
        observer1 = Observer(referee)
        self.assertTrue(len(referee.observers) == 1)
        self.assertTrue(type(referee.observers[0]) == Observer)

    def test_observer(self):
        referee = Referee(Board(), self.player1, self.player2)
        observer1 = Observer(referee)
        with self.captured_output() as (out, err):
            referee.update_observers(Action.MESSAGE,'hello')
        output = out.getvalue().strip()
        self.assertEqual(output, '"hello"')

    def test_observer_with_placement_looping_player(self):
        player_never_return = TestReferee.PlayerNeverReturn("abc", self.strategy)
        referee = Referee(Board(), self.player1, player_never_return)
        observer = Observer(referee)
        with self.captured_output() as (out, err):
            referee.run_game(self.rulechecker)
        output = out.getvalue().strip()
        self.assertTrue("ian wins. abc timed out" in output)

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err
    
    class PlayerNeverReturn(Player):
        def place_worker(self, cur_board):
            while 1:
                x = 1
        def play_turn(self, cur_board):
            while 1:
                x = 1

    class ReturnNonsense(Player):
        def place_worker(self, cur_board):
            return 0

        def play_turn(self, cur_board):
            return 0


