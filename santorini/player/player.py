"""Player data representation in Santorini"""
import os
import sys
from santorini.aux.misbehaviors import Misbehaviors
from santorini.design.iplayer import AbstractPlayer
from santorini.common.worker import Worker
from santorini.common.rulechecker import RuleChecker


class Player:
    """Player representation in Santorini."""

    def __init__(self, name, strategy):
        """Create a Player.

        :param str name: the user's input name for the game
        :param AbstractStrategy strategy: any strategy object
        """
        self.name = name
        self.strategy = strategy
        self.rulechecker = RuleChecker()

    def place_worker(self, cur_board):
        """Worker Placement.

        This will be called with a copy of the board when it is this player's
        turn to place.

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

        p_workers = cur_board.player_workers[self.name] if self.name in cur_board.player_workers else []
        new_worker = Worker(self.name, 1 if len(p_workers) == 0 else 2)
        
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
        #print('board.player_workers: ', cur_board.player_workers.keys())
        #print("player's workers: ", cur_board.player_workers[self.name])
        p_workers = cur_board.player_workers[self.name]
        return self.strategy.plan_turn(p_workers, cur_board, self.name)
    
    def misbehaved(self):
        """Inform player what misbehavior caused its failure of the game

        """
        pass
    
    def set_name(self, new_name):
        self.name = new_name

    def match_begin(self, opname):
        """ inform player that a match with a opponent has begun

        :param str opname: the name of opponent
        """
        pass

    def tournament_result(self, result):
        """ inform player the result of tournament

        :param list result: [EncounterOutcome, ...] where EncounterOutcome is one of the following:
            - [String, String], which is the name of the winner followed by the loser
            - [String, String, "irregular"], which is like the first alternative but signals that the
               losing player misbehaved
        """
        pass