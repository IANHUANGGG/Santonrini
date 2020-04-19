"""Player data representation in Santorini"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from santorini.design.iplayer import AbstractPlayer
from santorini.common.rulechecker import RuleChecker
from santorini.common.worker import Worker
from santorini.player.loop_placement_strat import LoopPlacement
from santorini.player.tree_strat import TreeStrategy
from santorini.player.strategy import Strategy
from santorini.player.player import Player



class LoopingPlayer(Player):
    """Player would stuck in infinite loop in place_worker."""

    def __init__(self, name):
        """Create a Player.

        :param str name: the user's input name for the game
        :param AbstractStrategy strategy: any strategy object
        """
        self.name = name
        self.workers = []  # List of two workers
        self.strategy = Strategy(LoopPlacement(),TreeStrategy())
        self.rulechecker = RuleChecker()
        self.opponent = ""

