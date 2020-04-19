import unittest
import copy
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../Santorini"))
from contextlib import contextmanager
from io import StringIO
import sys
from santorini.admin.referee import Referee
from santorini.admin.tournament_manager import TournamentManager
from santorini.common.board import Board
from santorini.common.rulechecker import RuleChecker
from santorini.observer.observer import Observer
from santorini.observer.action import Action
from santorini.player.breaking_player import BreakingPlayer
from santorini.player.player import Player
from santorini.player.place_strat import PlaceStratDiagonal, PlaceStratFar
from santorini.player.strategy import Strategy
from santorini.player.tree_strat import TreeStrategy

class TestManager(unittest.TestCase):
    """Tests for the Referee component."""

    def setUp(self):
        self.filepath_1 = "../11/santorini.rc/1-in.json"
        self.filepath_2 = "../11/santorini.rc/2-in.json"
        self.filepath_3 = "../11/santorini.rc/3-in.json"
        self.rulechecker = RuleChecker()
    
    def test_manager_run_game1(self):
        manager = TournamentManager(self.filepath_1)
        results = manager.run_tournament(self.rulechecker)
        expected_misbehaviors = ["turn_loop1", "place_loop1", "turn_loop2", "place_loop2", "turn_loop3"]
        expected_meetups = [["good1", "turn_loop1"], ["good2", "good1"],
                ["good1", "place_loop1"], ["good1", "turn_loop2"], ["good3",
                    "good1"], ["good1", "place_loop2"], ["good1", "turn_loop3"], ["good3", "good2"]]
        self.assertEqual(json.dumps(results[0]),
                json.dumps(expected_misbehaviors))
        self.assertEqual(json.dumps(results[1]), json.dumps(expected_meetups))

    def test_manager_run_game2(self):
        manager = TournamentManager(self.filepath_2)
        results = manager.run_tournament(self.rulechecker)

        expected_misbehaviors = ["place_loop1", "turn_loop2"]
        expected_meetups = [["good1", "place_loop1"], ["good1", "turn_loop2"]]
        self.assertEqual(json.dumps(results[0]),
                json.dumps(expected_misbehaviors))
        self.assertEqual(json.dumps(results[1]), json.dumps(expected_meetups))

    def test_manager_run_game3(self):
        manager = TournamentManager(self.filepath_3)
        results = manager.run_tournament(self.rulechecker)

        expected_misbehaviors = ["place_loop1", "turn_loop2"]
        expected_meetups = [["good1", "turn_loop2"]]
        self.assertEqual(json.dumps(results[0]),
                json.dumps(expected_misbehaviors))
        self.assertEqual(json.dumps(results[1]), json.dumps(expected_meetups))
