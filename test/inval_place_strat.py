"""Two placement strategy implementations."""
import math
from santorini.player.strategy import PlaceStrategy
from santorini.common.board import Board


class InvalidPlaceStratDiagonal(PlaceStrategy):
    """Implementation of invalid placement strategy."""

    @staticmethod
    def get_placement(worker, board):
        return (-1, -1)


class InvalidPlaceStratFar(PlaceStrategy):
    """Implementation of timeout placement strategy."""

    @staticmethod
    def calc_distance(point1, point2):
        pass

    @staticmethod
    def get_farthest_pos(board, opposing_workers):
        pass

    @staticmethod
    def get_placement(worker, board):
        return (-1, -1)