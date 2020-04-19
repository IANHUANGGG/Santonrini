"""Two placement strategy implementations."""
import math
from santorini.aux.settings import BOARD_SIZE
from santorini.player.strategy import PlaceStrategy
from santorini.common.board import Board


class PlaceStratDiagonal(PlaceStrategy):
    """Implementation of diagonal placement strategy."""

    @staticmethod
    def get_placement(worker, board):
        """Return a valid placement of (row, col) for workers on the board.

        For these workers, they will be placed along the diagonal starting at
        (0,0) if the position on the board isn't occupied
        :param Worker worker: A given worker
        :param Board board: A game board
        :rtype pos (row, col): A location on the game board
        """
        place = (0, 0)
        for i in range(BOARD_SIZE):
            if not board.is_occupied((i, i)):
                place = (i, i)
                break
        return place


class PlaceStratFar(PlaceStrategy):
    """Implementation of "as far away" placement strategy."""

    @staticmethod
    def calc_distance(point1, point2):
        """Calculate the total distance between two positions.
        :param (int, int) point1: The first point
        :param (int, int) point2: The second point
        :rtype float: the calculated geometric distance
        """
        x_1, y_1 = point1
        x_2, y_2 = point2
        return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

    @staticmethod
    def get_farthest_pos(board, opposing_workers):
        """Return the farthest unoccipied board position.

        This position is calculated from any other opposing worker.

        :param Board board: A game board
        :param list Worker opposing_workers: A list of opposing workers
        :rtype pos (row, col): A location on the board
        """
        empty_board = [[0 for col in range(BOARD_SIZE)]
                       for row in range(BOARD_SIZE)]

        farthest_pos = (0, 0)
        farthest_dist = 0

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                low_dist = BOARD_SIZE * 2
                for worker in opposing_workers:
                    dist = PlaceStratFar.calc_distance((row, col), worker)
                    if dist < low_dist:
                        low_dist = dist
                empty_board[row][col] = low_dist
                if (farthest_dist < low_dist and
                        not board.is_occupied((row, col))):
                    farthest_pos = (row, col)
                    farthest_dist = low_dist
        return farthest_pos

    @staticmethod
    def get_placement(worker, board):
        """Return a valid placement of (row, col) for workers on the board.

        For these workers, they will be placed as far apart as possible from
        the other player's workers through the notion of geometric distance
        :param Worker worker: a given worker
        :param Board board: a game board
        :rtype pos (row, col): A location on the game board
        """
        opposing_workers = [board.worker_position(w) for w in board.workers
                            if w.player != worker.player]
        return PlaceStratFar.get_farthest_pos(board, opposing_workers)
