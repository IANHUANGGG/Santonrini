"""Interface for a RuleChecker in Santorini."""
from abc import ABC, abstractmethod

"""
A build or move request is a (Worker, Direction)

A Worker object is an instance of a worker on the board
A Direction object is an instance of a cardinal direction on the board
"""

class AbstractRuleChecker(ABC):
    """An interface to implement a rule checking module for Santorini.

    This module will incorporate all of the rules we have been given for
    this version of Santorini.
    """

    @abstractmethod
    def can_build(self, board, worker, direction):  # pragma: no cover
        """Check if a worker can build at the given position.

        A Worker can only build in an eight cell radius inside the board
        boundaries (6x6). They cannot build on a building with four floors.
        A Worker cannot build on a building with another worker on it.

        :param Board board to check with
        :param Worker worker to check with
        :param Direction direction the direction the worker wants to build at

        :rtype bool: Returns if the given worker can build at the given
        direction.
        """
        pass

    @abstractmethod
    def can_move(self, board, worker, direction):  # pragma: no cover
        """Check if a worker can move to the given position.

        A Worker can move to the eight of the neighboring fields if there are
        no other workers on the target or if there is a building on the target,
        its height must be at most one higher than the current worker height.
        A Worker can fall down a height of any length.
        A Worker may not be placed outside of the board boundaries (6x6).

        :param Board board to check with
        :param Worker worker to check with
        :param Direction direction the worker wants to move to

        :rtype bool: Returns if the given worker can move to the given
        direction.
        """
        pass
