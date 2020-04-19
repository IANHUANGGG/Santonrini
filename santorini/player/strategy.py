"""A strategy to be used with a Player component in Santorini."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from abc import ABC, abstractmethod
from santorini.design.istrategy import AbstractStrategy


# Strategies we have thought of so far:
#    * Aggressive: play next to the opposing player, try to cut them off, etc
#    * Passive: play far away from the opposing player, don't rush a build
#    * Quick: play to build to 3 the fastest


class Strategy(AbstractStrategy):
    """interface for a strategy object in Santorini."""

    def __init__(self, place_strat, turn_strat):  
        """Create a strategy to be used in Santorini."""
        self.place_strat = place_strat
        self.turn_strat = turn_strat

    def plan_placement(self, worker, board):
        """Generate a plan for the next turn to be played.

        :param Worker worker: a worker belonging to the player calling this method
        :param Board board: a copy of the current game board
        :rtype tuple result: a tuple containing a worker and a position
        (row, col), representing the placement on the board
        """
        return self.place_strat.get_placement(worker, board)

    def plan_turn(self, workers, board, player_id):
        """Generate a plan for the next turn to be played.

        :param list Worker workers: list of workers belonging to the player
        calling this method
        :param Board board: a copy of the current game board
        :rtype tuple result: a tuple containing a move and build request,
        representing a player's full turn
        """
        return self.turn_strat.get_turn(workers, board, player_id)


class PlaceStrategy(ABC):
    """An interface for a placement strategy."""

    @abstractmethod
    def get_placement(self, worker, board):
        """Return a valid placement of (row, col) for a worker on the board."""
        pass


class TurnStrategy(ABC):
    """An interface for a turn strategy."""

    @abstractmethod
    def get_turn(self, workers, board, player_id):
        """Return a valid turn for a worker on the board.

        A valid turn is one of:
        (None, None, None) - A no request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request
        """
        pass
