from enum import Enum

class Action(Enum):
    """ Represent the situation in a game.

    Action.BOARD represents the observer is being passed in a Board.board
    Action.PLACEMENT represents a placement request by a player
    Action.MOVE_BUILD represents a move/build request for a move/build by a
    player
    Action.WINNING_MOVE represents a winning move for a game
    Action.MESSAGE represents an timeout error of a final result notification
    """
    BOARD = 0
    PLACEMENT = 1
    MOVE_BUILD = 2
    MESSAGE = 3
    RESULTS = 4
