"""A game tree-based strategy to be used with a Player component in Santorini."""

import copy
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from itertools import product

from santorini.player.strategy import TurnStrategy
from santorini.common.direction import Direction


class BrokenStrategy(TurnStrategy):
    """A strategy implementation that is broken."""

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
                yield (worker, move_dir, build_dir)

    @staticmethod
    def set_workers(board, from_op, player, opponent):
        if from_op:
            return [w for w in board.workers if opponent != w.player]
        else:
            return [w for w in board.workers if player != w.player]


    def get_turn(self, workers, board, player_id):
        """Return a non-valid turn for the list of player's worker on the board.

        """
        turn = (None, None, None)
        for worker, move_dir, build_dir in BrokenStrategy.next_turn(workers, board):
            turn = (worker, move_dir, build_dir)
            break
        return turn
