"""Player misbehaviors for Santorini."""
from enum import Enum

class Misbehaviors(Enum):
    """Defines the type of player misbehaviors."""
    NORMAL = 0
    TIMEOUT = 1
    INVALIDCOMMAND = 2

    def misbehave_msg(self):
        """Returns the corresponding message for the misbehavior.

        :return str: message in string format
        """
        if self.value == 1:
            return "timed out"
        elif self.value == 2:
            return "broke the rules"
