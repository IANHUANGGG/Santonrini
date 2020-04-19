"""Player data representation in Santorini"""
import sys
import os
from santorini.design.iplayer import AbstractPlayer
from santorini.common.rulechecker import RuleChecker
from santorini.common.worker import Worker
from santorini.player.place_strat import PlaceStratDiagonal
from santorini.player.tree_strat import TreeStrategy
from santorini.player.strategy import Strategy
from santorini.player.player import Player


class GoodPlayer(Player):
    """Good behaving Player data representation in Santorini."""

    def __init__(self, name):
        """Create a Player.

        :param str name: the user's input name for the game
        :param AbstractStrategy strategy: any strategy object
        """
        self.name = name
        self.workers = []  # List of two workers
        self.strategy = Strategy(PlaceStratDiagonal(),TreeStrategy(1))
        self.rulechecker = RuleChecker()
        self.opponent = ""
