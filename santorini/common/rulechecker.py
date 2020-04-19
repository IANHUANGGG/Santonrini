"""A Rule checker implementation for Santorini."""
import copy
import itertools
from santorini.common.building import Building
from santorini.common.direction import Direction
from santorini.design.irulechecker import AbstractRuleChecker
from santorini.aux.settings import TOTAL_NUM_WORKERS, MOVE_HEIGHT_DIFFERENCE, MAX_HEIGHT

# A build or move request is a (Worker, Direction)
# A Worker object is an instance of a worker on the board
# A Direction object is an instance of a cardinal direction on the board

class RuleChecker():
    """RuleChecker validating player's turns and enforcing rules in a game."""

    def valid_position(self, board, position):
        """Check the validity of  a worker destination on the board.

        If the position calculated from the worker and direction is
        invalid and occupied, return False

        :param Board board: a copy of the game board
        :param (row, col) position: a tuple representation of a position
        :return bool: check if given position is valid
        """
        try:
            board.assert_bounds(position) == False
        except IndexError:
            return False
        return position and not board.is_occupied(position)

    def height_difference(self, board, worker, direction):
        """Return if the worker can move in the direction.

        Direction must be within the height difference.
        """
        return (board.get_height(board.worker_position(worker), direction) -
                board.get_height(board.worker_position(worker), Direction.STAY) <=
                MOVE_HEIGHT_DIFFERENCE)


    def can_place_worker(self, board, player, worker, position):
        """Return if you can place a worker at the position.

        :param Board board: a copy of the board
        :param Worker worker: a Worker to place
        :param tuple (row, col): a position to place the worker at
        """
        return (self.valid_position(board, position) and
                len(board.workers) < TOTAL_NUM_WORKERS and
                not board.worker_position(worker) and 
                self.ownership(worker, player))

    def can_move_build(self, board, player, worker, move_dir, build_dir=None):
        """Check if a worker can move and then build in the specified direction.

        :param Board board: a copy of the game board
        :param Worker worker: a Worker on the board
        :param Direction move_dir: A Direction to move in
        :param Direction build_dir: An (optional) Direction to build in
        """
        if (move_dir == None or move_dir == Direction.STAY 
            or build_dir == None or build_dir ==Direction.STAY):
            return False 
        moved_pos = Direction.move_position(board.worker_position(worker),
                                            move_dir)
        board_copy = copy.deepcopy(board)
        can_move = (self.valid_position(board_copy, moved_pos) and
                    self.height_difference(board, worker, move_dir))
        if can_move:
            board_copy.move_worker(worker, move_dir)
            if  (not build_dir or
                (self.valid_position(board_copy,
                Direction.move_position(moved_pos,build_dir)) and
                not board.is_maxheight(moved_pos, build_dir))):
                return self.ownership(worker, player)

    def is_game_over(self, board, player_name):
        """Determine if the game is over based on board state.

        Called by the referee while executing every move and build for a 
        player. If this is True at any point, after a move or build from 
        any player, the referee ends the game.

        Game-ending conditions:
        * A worker is on a building of height 3 = the player has won
        * A worker can move but not build = the game is not over
        * A worker can't move but can build = the game is not over

        :param Board board: a copy of the game board
        :param str player_name: name of the player to check is_game_over() for
        """
        if board.workers == []:
            return False
        turn_dict = {w: False for w in board.player_workers[player_name]}
        for worker in turn_dict.keys():
            # If any of the workers are at a height of 3, the game is over
            if (board.get_height(board.worker_position(worker), Direction.STAY) ==
                    (MAX_HEIGHT - 1)):
                board.winner = worker.player
                return True
            
            for move, build in itertools.product(Direction, Direction):
                if self.can_move_build(board, worker.player, worker, move, build):
                    turn_dict[worker] = turn_dict[worker] or True
                    break

        return not any(turn_dict.values())

    def get_winner(self, board):
        """Return the winning player given the game board

        If there is no winning player, this will return false

        :param Board board: a copy of the game board
        :returns Player | False: player if there is a winner,
        false if the game isn't over yet
        """
        game_over_both = True
        for player in board.players:
            game_over_both = game_over_both and not self.is_game_over(board,
                    player)

        if game_over_both:
            return False

        worker_status = {w.player: [] for w in board.workers}

        for worker in board.workers:
            worker_status[worker.player].append(False)

        for worker in board.workers:
            worker_pos = board.worker_position(worker)
            if board.get_height(worker_pos, Direction.STAY) == (MAX_HEIGHT - 1):
                return worker.player
            for move_dir in Direction:
                if self.can_move_build(board, worker.player, worker, move_dir):
                    worker_status[worker.player][worker.number - 1] = True

        for player in worker_status:
            if not any(worker_status[player]):
                return (worker_status.keys() - [player]).pop()
        return False

    def ownership(self, worker, player_input):
        return worker.player == player_input
