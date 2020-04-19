from santorini.player.strategy import PlaceStrategy
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
class LoopPlacement(PlaceStrategy):
    """An interface for a placement strategy."""

    def get_placement(self, worker, board):  # pragma: no cover
        """Return a valid placement of (row, col) for a worker on the board."""
        while 1:
            x = 1