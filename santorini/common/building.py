from santorini.aux.settings import MAX_HEIGHT


class Building:
    """A game piece representing a building in Santorini.""" 

    def __init__(self, floor=0):
        """Create a building with 0 floors."""
        self._floor = floor

    def __str__(self):
        return self._floor

    def build(self):
        """Build a floor in the current building.

        Increments floor each time this is called if the number
        of floors in this building is less than four.

        :rtype int returns the new height of the building
        :raise OverflowError: if a Worker tries to add a fifth
        floor to a building
        """
        if self.is_max_height():
            raise OverflowError("Cannot build over {}".format(MAX_HEIGHT))
        else:
            self._floor += 1

    @property
    def floor(self):
        """Return number of floors in the building."""
        return self._floor

    def is_max_height(self):
        """Return True if it is at the max height."""
        return self._floor == MAX_HEIGHT