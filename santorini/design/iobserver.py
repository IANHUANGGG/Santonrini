#!/usr/bin/python3
"""Interface for observer."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from abc import ABC, abstractmethod


class IObserver(ABC):
    """Interface for observer of referee."""

    @abstractmethod
    def update(self, message):
        """ Update the observers of referee's actions.
        Called by the Referee when it decides it is time to update
        the observers. 

        :param observerable: Observable object being observed
        """
        pass

