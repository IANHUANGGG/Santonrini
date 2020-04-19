"""Observer to be used to observe the Referee"""
import json
from santorini.common.direction import Direction
from santorini.observer.action import Action
from santorini.design.iobserver import IObserver


class Observer(IObserver):
    """Interface for observer of referee.
    
        Observer observes its registered Observable. 
        Whenever, the Observable-inherited object calls
        notify_observers(), the observers are updated."""

    def __init__(self, name):
        """ Register self to the observable.
        
        :param Observable observable: the Referee to observed
        """
        self.name = name

    def update(self, action, message):
        """ Update the observers of referee's actions.
        Called by the Referee when it decides it is time to update
        the observers. Message is either a worker placement, move/build, board
        copy, 

        :param Action action: Type of object being observed
        :param message: Tuple/message in str depending on action
        """
        #print("Observer: ", self.name)
        if message == None:
            return 
        elif action == Action.BOARD:
            print(self.parse_board(message))
        elif action == Action.PLACEMENT:
            print(self.parse_placement(message))
        elif action == Action.MOVE_BUILD:
            print(self.parse_move_build(message))
        elif action == Action.MESSAGE:
            print(self.parse_message(message))
        elif action == Action.RESULTS:
            print(self.parse_results(message))

    def parse_board(self, board):
        """Given a list of list of Buildings, parse it into JSON.

        :param Board board: board copy
        """
        return board.board_into_list()
        
    def parse_placement(self, placement):
        """Given a placement, return its JSON representation.
        placement is given in the form of (Worker, (row, col)).
        returned JSON should be in the form [Worker, row, col]

        :param Tuple placement: placement tuple
        """
        worker = placement[0].player + str(placement[0].number)
        representation = [worker, placement[1][0], placement[1][1]]
        return json.dumps(representation)

    def parse_move_build(self, turn):
        """ Given a turn, return the Action representation in JSON.
        turn is given in the form of (Worker, Direction, Direction).

        :param Tuple turn: turn tuple
        """
        worker = turn[0].player + str(turn[0].number)
        move = Direction.separate_ew_ns(turn[1])
        build = Direction.separate_ew_ns(turn[2])
        representation = [worker,move[0],move[1],build[0],build[1]] 
        return json.dumps(representation)

    def parse_message(self, message):
        """ Given a message/error, return its JSON representation

        :param str message: error for final result message
        """
        return json.dumps(message)

    def parse_results(self, results):
        sb = []
        for result in results:
            if len(result) == 2:
                sb.append(result[0] + " won, " + result[1] + " lost" + "\n")
            elif len(result) == 3:
                sb.append(result[0] + "won, " + result[1] + " misbehaved" + "\n")
        return ''.join(sb)
    

