from santorini.aux.settings import BOARD_SIZE
from santorini.common.building import Building
from santorini.common.direction import Direction
from santorini.design.iboard import AbstractBoard
from santorini.common.worker import Worker

class Board(AbstractBoard):
    """Board implementation for Santorini."""

    def __init__(self, board=None, workers=None):
        """Create a 6x6 board. with 0-floor buildings in each cell.

        _board is a 2-d array of Buildings representing the Santorini board,

        _workers is a dictionary of Workers to Position (ROW, COLUMN) on board
        """
        self.player_workers = {}
        self.players = []
        self._workers = {}
        if board:
            self.parse_board_list(board)
        else:
            self._board = [[Building() for col in range(BOARD_SIZE)]
                           for row in range(BOARD_SIZE)]

        if workers:
            self._workers = workers

            for worker in workers.keys():
                self.players.append(worker.player)
                if worker.player not in self.player_workers:
                    self.player_workers[worker.player] = [worker]
                else:
                    self.player_workers[worker.player].append(worker)
        
    @property
    def workers(self):
        """Return the list of workers on this board."""
        return list(self._workers.keys())

    def assert_bounds(self, pos):
        """Raise an exception if the position is out of bounds.

        :param tuple (row, col): A position on the game board
        :raises IndexError: if the position is outside of the board
        range [0,BOARD_SIZE)
        """
        row, col = pos

        #return row in range(BOARD_SIZE) and col in range(BOARD_SIZE)

        if not (row in range(BOARD_SIZE) and
                col in range(BOARD_SIZE)):
            raise IndexError("Cannot place a worker out of board bounds")

    def place_worker(self, worker, pos):
        """Place a worker in a starting position on the board.

        Update the current dictionary of workers to set the input worker's 
        position to the new input pos

        :param Worker worker: a Worker object
        :param tuple (row, col): a position on the board
        :raises IndexError: if the position is outside of the board
        range [0,BOARD_SIZE)
        """
        self.assert_bounds(pos)
        self._workers[worker] = pos
        if not worker.player in self.players:
            self.players.append(worker.player)

        if worker.player in self.player_workers:
            if len(self.player_workers[worker.player]) < 2:
                self.player_workers[worker.player].append(worker)
        else:
            self.player_workers[worker.player] = [worker]

    def move_worker(self, worker, direction):
        """Move a worker to a new position on the board.

        Update the worker's position in the internal dictionary 
        to the new positioncalculated from the given direction

        :param Worker worker: a Worker on the board
        :param Direction direction: a Direction on the board
        :raise IndexError: if the calculated position is outside the bounds of
        the board
        :raise LookupError: if the worker is not found on the board (i.e. in
        the _workers dict)
        :raise ValueError: if the calculated position is already occupied by
        another Worker
        """
        pos = self.worker_position(worker)
        cur_pos = Direction.move_position(pos, direction)
        self.assert_bounds(cur_pos)
        self._workers[worker] = cur_pos

    def build_floor(self, worker, direction):
        """Build one floor of a building at a position.

        Add a single floor to the given position.
        All valid positions on the board are buildings, starting
        at 0 floors. Increments the Building's floor counter by one

        Building on a position that already has 4 floors does nothing.

        :param Worker worker: a Worker on the board
        :param Direction direction: a Direction on the board
        :raise IndexError: if the calculated position is outside the bounds of
        the board
        :raise LookupError: if the worker is not found on the board (i.e. in
        the _workers dict)
        """
        pos = self.worker_position(worker)
        row, col = Direction.move_position(pos, direction)
        self.assert_bounds((row, col))
        self._board[row][col].build()

    def get_height(self, position, direction):
        """Get the height of a building.

        The height of a building is obtained from getting the
        input worker's position and adding the input direction to it

        :param Worker worker: a Worker on the board
        :param Direction direction: a Direction on the board
        :rtype int: the building height at the position
        :raise IndexError: if the calculated position is outside the bounds of
        the board
        :raise KeyError: if the worker is not found on the board (i.e. in
        the _workers dict)
        """
        row, col = Direction.move_position(position, direction)
        self.assert_bounds((row, col))
        return self._board[row][col].floor

    def new_wid(self, pid):
        """ return a new worker number which depends on if the player has placed a worker or not
        Arguments:
            pid {str} -- the name of player who request a new worker id
        Returns:
            int -- a worker id
        """

        if pid in self.player_workers:
            return len(self.player_workers[pid]) + 1
        else:
            return 1

    def is_maxheight(self, position, direction):
        """Return if location from worker pos & dir is at max height.

        :param Worker worker: a Worker on the board
        :param Direction direction: the direction the Worker is interested in
        :rtype bool: True if the desired building is at max height
        """
        row, col = Direction.move_position(position, direction)
        self.assert_bounds((row, col))
        return self._board[row][col].is_max_height()

    def worker_position(self, worker):
        """Return the position of the given worker as a (row, col).

        If the worker isn't found on the board, return None

        :param Worker worker: a Worker on the board

        :rtype tuple pos | None: the position (row, col) on the board
        the worker is at
        """
        return self._workers.get(worker)

    def is_occupied(self, pos):
        """Check if the current location is occupied by a Worker or out of bounds.

        :param Position (row, col): the position to check against
        :rtype bool: Returns if the position is not occupied and valid
        """
        return any([p == pos for p in self._workers.values()])

    def is_neighbor(self, worker, direction):
        """Check if the input worker has a neighbor.

        :param Worker worker: a Worker on the board
        :param Direction direction: the Direction the Worker wants to move
        :raises KeyError: if the worker is not in the dictionary
        :rtype bool
        """
        try:
            pos = self.worker_position(worker)
            self.assert_bounds(Direction.move_position(pos, direction))
        except IndexError:
            return False
        return True

    def board_into_list(self):
        """ Displays the list representation of the board.

        The returned list is a list of list of Cells. Each Cell is either a
        Height(int) or a BuildingWorker(Height followed by a Worker). Worker is
        the owning player name concantenated by worker number.
        """
        result = []

        for row in range(BOARD_SIZE):
            result.append([])
            for column in range(BOARD_SIZE):
                height = self._board[row][column]._floor
                result[row].append(height)

                for worker in self.workers:
                    if self.worker_position(worker) == (row,column):
                        str_height = str(self._board[row][column]._floor)
                        worker_repr = str_height + worker.player + str(worker._num)
                        result[row][column] = worker_repr

        return result

    def parse_board_list(self, board_list):
        self._board = []
        for row in range(BOARD_SIZE):
            self._board.append([])
            for col in range(BOARD_SIZE):
                try:
                    cell = board_list[row][col]
                    height = 0
                    if type(cell) == int:
                        height = int(cell)
                    else:
                        height = int(cell[0])
                        player_id = cell[1:-1]
                        worker_num = int(cell[-1])
                        worker = Worker(player_id, worker_num)
                        self._workers[worker] = (row, col)
                        if player_id not in self.player_workers:
                            self.player_workers[player_id] = [worker]
                        else:
                            self.player_workers[player_id].append(worker)
                            self.players.append(player_id)
                except IndexError:
                    height = 0
                self._board[row].append(Building(height))