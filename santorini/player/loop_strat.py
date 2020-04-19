"""A game tree-based strategy to be used with a Player component in Santorini."""

import copy
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from itertools import product
import time

from santorini.player.strategy import TurnStrategy
from santorini.common.direction import Direction
from santorini.common.rulechecker import RuleChecker


class LoopStrategy(TurnStrategy):
    """A strategy implementation that uses a game tree to ensure that
    the opponent cannot make a winning move given a depth to look-ahead
    in the tree
    """

    def get_turn(self, workers, board, player_id):
        time.sleep(12)
