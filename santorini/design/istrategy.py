"""Interface for a Strategy in Santorini."""
from abc import ABC, abstractmethod


class AbstractStrategy(ABC):
    """interface for a strategy object in Santorini."""

    @abstractmethod
    def plan_placement(self, workers, board):
        """Generate a plan for the next turn to be played.

        :param list Workers: a list of workers belonging to the player
        calling this method
        :param Board board: a copy of the current game board
        :rtype tuple result: a tuple containing a worker and a position
        (row, col), representing the placement on the board
        """
        pass

    @abstractmethod
    def plan_turn(self, workers, board):
        """Generate a plan for the next turn to be played.

        :param list Workers: a list of workers belonging to the player
        calling this method
        :param Board board: a copy of the current game board
        :rtype tuple result: a tuple containing a move and build request,
        representing a player's full turn
        """
        pass
