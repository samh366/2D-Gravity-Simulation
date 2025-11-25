from decimal import Decimal
from enum import Enum

from gravity_sim.object import Object
from gravity_sim.vector import Vector


class Direction(Enum):
    """Enum to store the 4 intercardinal directions."""
    NW = 1
    NE = 2
    SW = 3
    SE = 4

class QuadTree:
    """A Quad-Tree implementation for the Barnes-Hut algorithm."""
    def __init__(self, center: Vector, width: Decimal):
        """Create a new empty quad tree."""
        self.center = center
        self.width = Decimal(width)

        self.value = None
        self.mass = Decimal(0)
        self.corners: dict[Direction, QuadTree] = {
            Direction.NW: None,
            Direction.NE: None,
            Direction.SW: None,
            Direction.SE: None
        }

    def insert_object(self, obj: Object) -> None:
        """Insert an object into the QuadTree correctly.

        Args:
            obj (Object): The object to insert.
        """
        self.mass += obj.mass
        if self.value is None:
            self.value = obj
            return

        x, y = obj.get_position()
        if x <= self.center and y >= self.center:
            self.add_to_lower_quad_tree(Direction.NW, obj)
        if x > self.center and y >= self.center:
            self.add_to_lower_quad_tree(Direction.NE, obj)
        if x <= self.center and y < self.center:
            self.add_to_lower_quad_tree(Direction.SW, obj)
        if x > self.center and y < self.center:
            self.add_to_lower_quad_tree(Direction.SE, obj)


    def add_to_lower_quad_tree(self, direction: Direction, obj: Object) -> None:
        """Add an object to one of this QuadTree's children.

        Args:
            direction (Direction): The direction of the quad tree to add it to.
            obj (Object): The object to add.
        """
        if self.corners[direction] is None:
            self.corners[direction] = QuadTree(center=self.calc_new_center(direction), width=self.width/2)
        self.corners[direction].insert_object(obj)

    def calc_new_center(self, direction: Direction) -> Decimal:
        """Calculate the center of the quadrant in the provided direction based on this QuadTree's center.

        Args:
            direction (Direction): The direction of the QuadTree to calculate it's center.

        Returns:
            Decimal: The calculated center.
        """
        width = self.width / 2
        transformation = Vector()
        match direction:
            case Direction.NW:
                transformation = Vector(-width, width)
            case Direction.NE:
                transformation = Vector(width, width)
            case Direction.SW:
                transformation = Vector(-width, -width)
            case Direction.SE:
                transformation = Vector(width, -width)
        return self.center + transformation