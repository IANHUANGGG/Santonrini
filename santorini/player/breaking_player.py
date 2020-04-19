"""Player data representation in Santorini"""
import sys
import os
from santorini.common.rulechecker import RuleChecker
from santorini.common.worker import Worker
from santorini.design.iplayer import AbstractPlayer
from santorini.player.broken_strat import BrokenStrategy
from santorini.player.place_strat import PlaceStratDiagonal
from santorini.player.strategy import Strategy


class BreakingPlayer:
    """Misbehaving Player data representation in Santorini."""

    def __init__(self, name):
        """Create a Player.

        :param str name: the user's input name for the game
        :param AbstractStrategy strategy: any strategy object
        """
        self.name = name
        self.workers = []  # List of two workers
        self.strategy = Strategy(PlaceStratDiagonal(),BrokenStrategy())
        self.rulechecker = RuleChecker()
        self.opponent = ""

    def place_worker(self, cur_board):
        """Worker Placement.

        This will be called with a copy of the board when it is this player's
        turn to place. Worker placement for BrokenPlayer is valid.
        
        The board contains a dictionary of workers mapped to their positions,
        and each worker knows which player it is associated with. When a
        player places a worker, its position is updated in this dictionary in
        the next placement turn.
        The board also contains all of the heights of the buildings on the
        board. Interacting with this board *will not* change the current state
        of the board.

        To place a worker, the player will send the board state to the strategy
        object and receive a placement. A placement is a tuple of worker and
        positon (in the form ( Worker, (row, col)),
        representing the placement of a single worker on the board.

        After receiving this placement, the player will send this to the
        referre. If the placement is invalid or breaks the rules according
        to our defined rulechecker, the referee will call is_gameover and
        automatically declare the opposing player the winner.

        If the placement is valid, the referee will execute the placement and
        send back an updated version of the board for the next placement.

        When the placement is over, the referee will transition the player to a
        play turn when this player has both of its workers place and there are
        a total of four workers on the board.

        :param Board cur_board: a copy of the current board
        """
        #place workers
        if not self.workers: # if self.workers is empty
            new_worker = Worker(self.name,1)
        elif len(self.workers) < 2: # if the player already has one worker
            new_worker = Worker(self.name,2)
            
        self.workers.append(new_worker)
        
        return tuple((new_worker, self.strategy.plan_placement(new_worker,cur_board)))

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        This will be called with a copy of the board when it is this player's
        turn.

        The board contains a dictionary of workers mapped to their positions,
        and each worker knows which player it is associated with.

        The board also contains all of the heights of the buildings on the
        board

        Interacting with this board *will not* change the current state of the
        board

        To play a turn, the player will send the board state to the strategy
        object and receive a turn. A turn is a tuple of tuples
        (in the form ((Worker, Direction), (Worker, Direction)),
        representing a move request and a build request in the game. The first
        item in the tuple represents a move request with a worker and a
        direction, and the second item represents a build request with a worker
        and a direction.

        After receiving this turn, the player will send this to the referre.
        If the turn is invalid or breaks the rules according to our defined
        rulechecker,the referee will call is_gameover and automatically declare
        the opposing player the winner.

        If the turn is valid, the referee will execute the move and build
        requests and send back an updated version of the board on the next
        turn.

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        return self.strategy.plan_turn(self.workers, cur_board, self.name)

    def game_over(self, _winner):
        """Call when the game is over.

        If any of the endgame conditions are met (see is_gameover method
        in the rulechecker interface), this will be sent to the game
        to determine the winner of the game.

        The game will send back which player's name won the game based on
        endgame conditions and return this name to the player to compare to
        itself.

        :param str winner: the name of the Player that won the game
        """
        # reset
        self.workers = []
