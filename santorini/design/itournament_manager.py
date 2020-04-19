"""Tournament Manager Interface to manage tournaments."""
from abc import ABC, abstractmethod


class ITournamentManager(ABC):
    """ Tournament Manager holds a fixed but arbirary number of players and runs
    a round-robin tournament of all players.

    The tournament function starts the tournament for all the players and outputs
    the winner. When a borken player is reached while the tournament manager is
    running the tournament, that broken player is automatically disqualified and
    its opponent is declared as the winner. In the case of both players in a
    game being broken, they are both disqualified and the tournament manager
    continues the tournament with the rest of the players. When the tournament
    has been ran and the winner determined, the tournament manager prints out
    the results starting from the winner to how many games each player has won.  
    """


    """ Runs a round-robin tournament of all players

        run_tournamenet initialize a dictionary--"tournament_result" where key is 
        player_id and value is a list of player_id whose defeated by this player.

        run_tournament use loops to get a pair of two players in players and initialize
        a referee to run best_of_n between two players. If there is n participated 
        players, the number of tournament between these players is (n+1)*(n/2) 
        = (n^2+n)/2 if all player function normally. Record the result of each 
        best_of_n in "tournament_result". 

        If a player is found being broken(throw exception, infinite loops), end the
        tournament it is in and remove this broken player from players and remove
        its id from tournament_result' keys and remove its id from other players
        defeated list to ensure fairness. 

        Report the result of tournament by returning "tournament_result" after all
        player has competed with each other once.

        :param List players a list of Player which will be completing with each other
        :param Int ngames Number of games in each tournament

        :rtype dict: Return tournament_result
    """

    @abstractmethod
    def run_tournament(self):
        """ Run the tournament.

        Run the tournament for all the players the tournament manager holds and
        output the winner and each player's game record.
        """
        pass

