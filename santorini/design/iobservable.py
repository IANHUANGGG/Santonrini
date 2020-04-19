"""Interface for the Observable in Santorini."""
from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

"""IObservable can be observed by any IObserver."""

class IObservable(ABC):
    """An interface to connect the observers.
    
    An observer is able to view the state of the board and the 
    player in turn if Observable is inherited by a Referee.
    """

    @abstractmethod
    def add_observer(self, observer):
        """Register an observer to the observable.

        :param Observer: observer
        """
        pass

    @abstractmethod
    def update_observers(self, action, message):
        """ Update all observers of gamestate/player misbehavior from the observable.

        :param Action action: type of action to be updated
        :param str message: message to be passed along
        """
        pass

