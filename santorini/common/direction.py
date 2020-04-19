from enum import Enum
from operator import add

class Direction(Enum):
    """Represents a direction in the eight cardinal directions.

    First entry in tuple is ROW, second entry is COLUMN

    STAY is equivalent of not moving to a new position
    """

    NORTH = (-1, 0)
    NORTHEAST = (-1, 1)
    NORTHWEST = (-1, -1)
    SOUTH = (1, 0)
    SOUTHEAST = (1, 1)
    SOUTHWEST = (1, -1)
    EAST = (0, 1)
    WEST = (0, -1)
    STAY = (0, 0)

    def __init__(self, row, col):
        """Create the Direction."""
        self.row = row
        self.col = col

    @property
    def vector(self):
        """Return the vector representation of the direction as (x, y)."""
        return (self.row, self.col)

    @staticmethod
    def move_position(pos, direction):
        """Return the new position as (row, col) given a direction to move in.

        :param pos (row, col):
        :param Direction direction:
        """
        #print("*************** pos: ", pos, " direction: ", direction)
        pos = tuple(map(add, pos, direction.vector))
        return pos

    @staticmethod
    def separate_ew_ns(direction):
        """ Given a direction, return a tuple with separated East/West,
        North/South.
        """
        if direction == Direction.NORTH:
            return ("PUT","NORTH")
        elif direction == Direction.NORTHEAST:
            return ("EAST","NORTH")
        elif direction == Direction.NORTHWEST:
            return ("WEST","NORTH")
        elif direction == Direction.SOUTH:
            return ("PUT","SOUTH")
        elif direction == Direction.SOUTHEAST:
            return ("EAST","SOUTH")
        elif direction == Direction.SOUTHWEST:
            return ("WEST","SOUTH")
        elif direction == Direction.EAST:
            return ("EAST","PUT")
        elif direction == Direction.WEST:
            return ("WEST","PUT")
        elif direction == Direction.STAY:
            return ("PUT","PUT")

    @staticmethod
    def str_to_dir(east_west, north_south):
        dir_tuple = (east_west, north_south)
        return TUPLE_TO_DIR[dir_tuple]


DIR_TO_TUPLE = {Direction.NORTH: ("PUT", "NORTH"), Direction.NORTHEAST: ("EAST","NORTH"),
            Direction.NORTHWEST: ("WEST","NORTH"), Direction.SOUTH: ("PUT","SOUTH"), 
            Direction.SOUTHEAST: ("EAST","SOUTH"), Direction.EAST: ("EAST","PUT"),
            Direction.WEST: ("WEST","PUT"), Direction.STAY: ("PUT","PUT"),
            Direction.SOUTHWEST: ("WEST","SOUTH")}
TUPLE_TO_DIR = {("PUT", "NORTH"): Direction.NORTH, ("EAST","NORTH"): Direction.NORTHEAST,
            ("WEST","NORTH"): Direction.NORTHWEST, ("PUT","SOUTH"): Direction.SOUTH, 
            ("EAST","SOUTH"): Direction.SOUTHEAST, ("EAST","PUT"): Direction.EAST,
            ("WEST","PUT"): Direction.WEST, ("PUT","PUT"): Direction.STAY,
            ("WEST","SOUTH"): Direction.SOUTHWEST}