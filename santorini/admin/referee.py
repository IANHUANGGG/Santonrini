"""Refereee component for Santorini."""
import copy
from santorini.aux import settings
from santorini.aux.misbehaviors import Misbehaviors
from santorini.aux.timeout import Timeout, TimeoutError
from santorini.common.rulechecker import RuleChecker
from santorini.design.iobservable import IObservable
from santorini.design.ireferee import AbstractReferee
from santorini.observer.action import Action
from santorini.common.board import Board


class Referee(AbstractReferee, IObservable):
    """ Referee oversee the gameplay of Santorini.

        The starting turn is given to player1 at index 0 of the list of players. 
        The turn alternates between two players until the game is over. The 
        order of the game turns is determined by the order of the player input
        when initializing the Referee. An instance of the Refereee can only 
        handle a game between two different players.
        """

    def __init__(self, board, player1, player2):
        """Create a referee component with the associated list of players.

        
        players: list of players in the game
        current_player: 0 or 1 index indicating the player in turn
        winner: name of the winning player

        :param Board board: current state of the board
        :param Player player1: player 1
        :param Player player2: player 2
        """
        self.board = board
        if player1.name == player2.name: 
            raise ValueError("Players cannot have the same name")
        self.players = [player1, player2]
        self.current_player = 0
        self.winner = None
        self.misbehaver = None
        self.misbehave_type = Misbehaviors.NORMAL
        self.observers = []

    def best_of(self, rounds, rulechecker):
        """Supervise a tournament between players.

        A referee runs a given number of game rounds, determining the winner
        that has won more rounds as the winner. If the given number of rounds 
        is an even integer, Referee adds one more round in order to make sure
        there is a winner. After every round, the winner is reset to None.
        Once the winner has been determined, it returns the name of the winning player.

        :param int rounds: number of rounds for the tournament
        :param Rulechecker rulechecker: rulechecker for the tournament
        :return tuple: a tuple (winner's name, misbehaver's name)
        """
        if rounds % 2 == 0:
            rounds += 1

        tournament = {}
        for player in self.players:
            tournament[player.name] = 0

        for _ in range(rounds):
            if self.misbehaver != None:
                break
            winner = self.run_game(rulechecker)
            tournament[winner] += 1
            self.winner == None
            self.board = Board()
            self.current_player = 0

        self.winner = max(tournament, key=tournament.get)
        return (self.winner, self.misbehaver)

    def run_game(self, rulechecker):
        """Supervise a game between players.

        The ref will receive the player's worker placements and then
        execute them in alternating order.

        If a game end state is reached, the referee returns the winner.
        """
        self.players[0].match_begin(self.players[1].name)
        self.players[1].match_begin(self.players[0].name)
        self.worker_placement(rulechecker)
        self.steady_state(rulechecker)
        self.inform_players()
        return self.winner

    def worker_placement(self, rulechecker):
        """ Retrieves, check legality and execute worker placement.

        If while returning a placement, the player in turn times out, then
        the player automatically loses the game and the other player is set
        as the winner. The same applies if a player returns an invalid
        placement.

        :param Rulechecker rulechecker: rulechecker
        """
        worker_placed = len(self.board.workers)
        while worker_placed < settings.TOTAL_NUM_WORKERS:
            board_copy = copy.deepcopy(self.board)
            player = self.players[self.current_player]

            try:
                with Timeout(settings.PLACEMENT_WAITTIME):
                    placement = player.place_worker(board_copy)
                    self.update_observers(Action.PLACEMENT, placement)
            except TimeoutError:
                self.broke_rule(Misbehaviors.TIMEOUT)
                return

            # verify placement
            if (type(placement) == tuple and len(placement) == 2):
                worker = placement[0]
                position = placement[1]
            #------
            elif placement == Misbehaviors.TIMEOUT:
                self.broke_rule(Misbehaviors.TIMEOUT)
                return
            #------
            else:
                self.broke_rule(Misbehaviors.INVALIDCOMMAND)
                return
        
            if rulechecker.can_place_worker(board_copy,
                                            player.name, 
                                            worker, 
                                            position):
                self.board.place_worker(copy.deepcopy(worker), position)
                self.update_observers(Action.BOARD, copy.deepcopy(self.board))
                worker_placed += 1

            self.current_player = 0 if self.current_player else 1

    def steady_state(self, rulechecker):
        """ Receive, check legality and execute alternating turns.

        :param Rulechecker rulechecker: rulechecker
        """

        while (self.winner == None and
               not rulechecker.is_game_over(self.board,
                   self.players[self.current_player].name)):
            player = self.players[self.current_player]
            opponent_idx = 0 if self.current_player else 1
            self.execute_turn(player, opponent_idx, rulechecker)
            self.current_player = opponent_idx

    def execute_turn(self, player, opponent_idx, rulechecker):
        """Complete a turn for a given player.

        If the turn is invalid, the ref will end the game and
        declare the opposing player as the winner.

        :param Player player: current player in turn
        :param int opponent_idx: index of the opponent player in self.players
        :param RuleChecker rulechecker: rulechecker
        """
        board_copy = copy.deepcopy(self.board)

        try:
            with Timeout(settings.TURN_WAITTIME):
                turn = player.play_turn(board_copy)

        except TimeoutError:
            self.broke_rule(Misbehaviors.TIMEOUT)
            return
#-------------
        if turn == player.name:
            self.winner = self.players[0 if self.current_player else 1].name
            self.update_observers(Action.MESSAGE,
                "{} wins. {} gave up".format(self.winner, player))
        elif type(turn) == tuple and len(turn) == 3:
            self.update_observers(Action.MOVE_BUILD, turn)
            worker = turn[0]
            move_dir = turn[1]
            build_dir = turn[2]

            if rulechecker.can_move_build(board_copy,
                                        player.name,
                                        worker, 
                                        move_dir, 
                                        build_dir):
                self.board.move_worker(worker, move_dir)
                self.board.build_floor(worker, build_dir)
                self.update_observers(Action.BOARD, copy.deepcopy(self.board))
            else:
                self.broke_rule(Misbehaviors.INVALIDCOMMAND)
        elif turn == Misbehaviors.TIMEOUT:
            self.broke_rule(Misbehaviors.TIMEOUT)
        else:
            self.broke_rule(Misbehaviors.INVALIDCOMMAND)
            

    def update_observers(self, action, message):
        """Update all observers registered to the Referee..

        If the observer times out while being updated, the timed out observer is
        removed from the Referee's list of observers and not updated anymore. 

        :param Action action: type of action to be updated
        :param str/board/turn/placment message: message 
        """
        for observer in self.observers:
            try:
                with Timeout(settings.OBSERVER_WAITTIME):
                    observer.update(action, message)
            except TimeoutError:
                self.observers.remove(observer)

    def add_observer(self, observer):
        """ Add an observer to the Referee.

        :param Observer observer: observer to be added to this Referee
        """
        if observer not in self.observers:
            self.observers.append(observer)

    def broke_rule(self, misbehave_type):
        """ Referee actions for the misbehaving player in current turn.
        
        Set its opponent as winner, and set the player in current turn as 
        misbehaver. Update observers with corresponding message.

        :param Misbehavior misbheave_type: type of misbehavior
        """
        self.winner = self.players[0 if self.current_player else 1].name
        self.misbehaver = self.players[self.current_player].name
        self.misbehave_type = misbehave_type
        message = misbehave_type.misbehave_msg()
        self.update_observers(Action.MESSAGE,
                "{} wins. {} {}.".format(self.winner, self.misbehaver, message))

    def inform_players(self):
        """Informs the players of game results."""
        #print("winner", self.winner)
        p = self.players
        winner_loser = (p[0], p[1]) if self.winner == self.players[0].name else (p[1], p[0])
        #print("win_lose", winner_loser)
        if self.misbehave_type.value == 2:
            winner_loser[1].misbehaved()
