import unittest
import json
from santorini.admin.referee import Referee
from santorini.common.board import Board
from santorini.common.direction import Direction
from santorini.common.worker import Worker
from santorini.player.player import Player
from santorini.design.iobserver import IObserver
from santorini.observer.observer import Observer
from santorini.player.place_strat import PlaceStratDiagonal
from santorini.player.strategy import Strategy
from santorini.player.tree_strat import TreeStrategy

class TestObserver(unittest.TestCase):

    def setUp(self):
        strategy = Strategy(PlaceStratDiagonal(), TreeStrategy())
        p1 = Player('p1',strategy)
        p2 = Player('p2',strategy)
        self.referee = Referee(Board(), p1, p2)
        self.observer = Observer(self.referee)

    def test_parse_board(self):
        board = self.observer.parse_board(Board())
        levels = [[floor !=  0 for floor in row] for row in board]
        self.assertFalse(any(any(row) for row in levels))

    def test_parse_placement(self):
        worker = Worker('p2',2)
        json_placement = self.observer.parse_placement((worker, (0, 0)))
        self.assertEqual(json_placement, json.dumps(["p22", 0, 0]))
        
    def test_parse_move_build(self):
        worker = Worker('p2',2)
        turn = (worker, Direction.NORTH, Direction.SOUTH)
        json_mb = self.observer.parse_move_build(turn)
        self.assertTrue(json_mb == json.dumps(['p22', 'PUT', 'NORTH', 'PUT', 'SOUTH']))

    def test_parse_message(self):
        json_msg = self.observer.parse_message('hello')
        self.assertTrue(json_msg == json.dumps('hello'))
