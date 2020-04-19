"""A game tree-based strategy to be used with a Player component in Santorini."""
import copy
from itertools import product

from santorini.player.strategy import TurnStrategy
from santorini.common.direction import Direction
from santorini.common.rulechecker import RuleChecker


class TreeStrategy(TurnStrategy):
    """A strategy implementation that uses a game tree to ensure that
    the opponent cannot make a winning move given a depth to look-ahead
    in the tree
    """

    def __init__(self, depth=2):
        """Constructs a Game-tree turn strategy object with the
        look-ahead depth

        :param int depth: the amount of turns to lookahead (defaults to 2)
        """
        self.depth = depth

    @staticmethod
    def next_turn(workers, board):
        """Creates a generator that yields the next possible
        turn given a list of workers and board

        :param list Worker workers: A list of workers belonging
                                    to the same player
        :param Board board: A game board
        :rtype Generator[(Worker, Direction, Direction), None None]
        """
        for worker in workers:
            for move_dir, build_dir in product(Direction, Direction):
                if (RuleChecker().can_move_build(board, worker.player, worker,
                                               move_dir, build_dir)):
                    yield (worker, move_dir, build_dir)

    @staticmethod
    def do_survive(board, depth, from_op, player, opponent, 
                    worker, move_dir, build_dir=None):
        """Given a game state, and a look-ahead depth and an
        optional turn, return whether or not the given player name
        survives up to the depth number of rounds.

        :param Board board: A game board
        :param str pname: A player name
        :param int depth: the number of look-ahead rounds
        :param Worker worker: an optional worker to move and/or build
        :param Direction move_dir: The direction to move the given
                                   worker if a worker was given
        :param Dircetion build_dir: An optional direction the worker builds in
        :param from_op: If this method is called from opponent' worker
        :rtype bool: if we survived depth number of rounds
        """

        if depth == 0: 
            return True
        if TreeStrategy.perform_move_build(board, worker, move_dir, build_dir) == False:
            return False

        next_workers = TreeStrategy.set_workers(board, from_op, player, opponent)
        next_turns = TreeStrategy.next_turn(next_workers, board)
        depth = depth - 1 
        if depth == 0:
            return True
        for next_worker, next_move, next_build in next_turns:

            if next_worker == None:
                return False
            board_copy = copy.deepcopy(board)
            if from_op:
                if TreeStrategy.do_survive(board_copy, depth, False, player, opponent, 
                                        next_worker, next_move, next_build):
                    return True
            else:
                if not TreeStrategy.do_survive(board_copy, depth, True, player, opponent, 
                                        next_worker, next_move, next_build):
                    return False
        return not from_op

    @staticmethod
    def set_workers(board, from_op, player, opponent):
        if from_op:
            return [w for w in board.workers if opponent != w.player]
        else:
            return [w for w in board.workers if player != w.player]

    @staticmethod
    def perform_move_build(board, worker, move_dir, build_dir):
        board.move_worker(worker, move_dir)
        if RuleChecker().get_winner(board):
            return False
        board.build_floor(worker, build_dir)
        return True

    def get_turn(self, workers, board, player_id):
        """Return a valid turn for the list of player's worker on the board.

        A valid turn is one of:
        (None, None, None) - A no request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request

        :param list Worker workers: A list of a player's worker
        :param Board board: a game board

        :rtype Union[str(Player_id), (Worker, Direction, None),
                     (Worker, Direction, Direction)]:
               a valid turn as described above
        """
        opponent = ''.join([x for x in board.players if x != player_id])
        turn = player_id
        for worker, move_dir, build_dir in TreeStrategy.next_turn(workers, board):
            boadr_copy = copy.deepcopy(board)
            if TreeStrategy.do_survive(boadr_copy, self.depth, False,
                                       player_id, opponent,
                                       worker, move_dir, build_dir):
                turn = (worker, move_dir, build_dir)
                break
        return turn
