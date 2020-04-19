from santorini.aux.settings import WORKER_NUM_PER_PLAYER

class Worker:
    """A game piece representing a worker in Santorini."""

    def __init__(self, player, num):
        """Create a worker.

        Worker will be associated with the player and the piece number
        given as inputs
        :param str player: the player this piece is associated with
        :param int num: the piece number [1 - NUM_WORKERS]
        :raises ValueError when num is out of range [1 - NUM_WORKERS]
        """
        self._player = player
        if num in range(1, WORKER_NUM_PER_PLAYER + 1):
            self._num = num
            self._name = self._player + str(self._num)
        else:
            raise ValueError("Worker number out of range!")

    @property
    def player(self):
        """Return the player the worker belongs to."""
        return self._player

    @property
    def number(self):
        """Return the piece number of the worker."""
        return self._num

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        """Worker piece equality."""
        if not isinstance(other, Worker):
            return False
        return (self._player == other.player and
                self._num == other.number)

    def __hash__(self):
        """Worker piece hashing."""
        return hash((self._player, self._num))
    
    def __repr__(self):
        return self._player + str(self._num)