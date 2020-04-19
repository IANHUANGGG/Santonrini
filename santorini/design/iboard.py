"""Interface for the Santorini board."""
from abc import ABC, abstractmethod

"""
Datatypes:
    A Worker is represented by a class and contains which player it belongs to.
    A Building is represented by a class and contains the number of floor it
    contains.
    A Position is represented by a tuple (int, int) which represents a location
    on the board.
"""

class AbstractBoard(ABC):
    """Abstsract Board for Santorini."""

    def __init__(self):
        """Create a 6x6 board. with 0-floor buildings in each cell.

        _board is a 2-d array of Buildings representing the Santorini board,

        _workers is a dictionary of Workers -> Position which represents their
        positions on the board.
        """
        self._board = [[]]
        self._workers = {}

    @property
    def workers(self):
        """Return the workers.

        :rtype dict: the dictionary mapping Workers -> Position
        """
        return self._workers

    @abstractmethod
    def place_worker(self, worker, pos):
        """Place a worker in a starting position on the board.

        If position is invalid or out of bounds, raise an exception

        :param Worker worker: a Worker on the board
        :param Position: a (x, y) position on the board
        :type Position: (int, int)
        :rtype Position: the new position of the worker
        """
        pass

    @abstractmethod
    def move_worker(self, worker, direction):
        """Move a worker to a new position on the board.

        move_worker moves the given worker to the given position.

        a Worker *must* be placed before it can move

        This does not check if a worker can move there.

        If position is invalid or out of bounds, raise an exception.

        :param Worker worker: a Worker on the board
        :param Position: a (x, y) position on the board
        :type Position: (int, int)
        :rtype Position: the new position of the worker
        """
        pass

    @abstractmethod
    def build_floor(self, worker, direction):
        """Build one floor of a building at a position.

        build_floor adds a single floor to the given position.
        All valid positions on the board are buildings, starting
        at 0 floors. Increments the Building's floor counter by one

        Building on a position that already has 4 floors does nothing.

        :param Position: a (x, y) position on the board that does
        not contain a worker
        :type Position: (int, int)
        :rtype int: the new floor count
        """
        pass
