"""Interface for a referee in Santorini."""
from abc import ABC, abstractmethod


class AbstractReferee(ABC):
    """Interface for a Referee component in Santorini."""

    def __init__(self, players):
        """Create a referee component with the associated list of players."""
        self.players = players

    @abstractmethod
    def best_of(self, rounds, rulechecker):
        """Supervise a tournament between players."""

        pass

    @abstractmethod
    def run_game(self):
        """Supervise a game between players.

        A referee will be able to construct a new board and have
        access to the rules. The ref will then initialize each player
        and then determine the "first" player in the game.

        The ref will receive the player's worker placements and then
        place them, in alternating order, on the board.

        During the course of the game, the ref will call complete_turn
        to execute turns given to him by the player.

        If a game end state is reached, the ref will call determine_winner
        to check against its list of players and the board to get the
        winner of the game. 
        """
        pass

    @abstractmethod
    def execute_turn(self, player):
        """Complete a turn for a given player.

        This method will call the player's play_turn method in
        conjunction with the rulechecker.

        If the turn is invalid, the ref will end the game and
        declare the opposing player as the winner.
        """
        pass
