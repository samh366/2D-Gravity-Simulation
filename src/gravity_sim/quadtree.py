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
        self.center_of_mass = None
        self.num_items = 0
        self.subtrees: dict[Direction, QuadTree] = {
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
        self.add_mass(obj)
        if self.num_items == 0:
            self.value = obj
            self.num_items += 1
            return
        if self.num_items == 1:
            # Move the current occupying item down to the next subtree too.
            self.add_to_subtree(self.value)
            self.value = None
        self.add_to_subtree(obj)
        self.num_items += 1

    def add_mass(self, obj: Object) -> None:
        """Update the total mass and center of mass of the node.

        Args:
            obj (Object): _description_
        """
        if self.mass == 0:
            self.mass = obj.mass
            self.center_of_mass = obj.position.copy()
            return

        x1, y1 = self.center_of_mass
        x2, y2 = obj.position
        m1 = self.mass
        m2 = obj.mass

        total_mass =  m1 + m2
        x = (x1*m1 + x2*m2) / total_mass
        y = (y1*m1 + y2*m2) / total_mass
        self.center_of_mass = Vector(x, y)
        self.mass = total_mass

    def add_to_subtree(self, obj: Object) -> None:
        """Add an object to one of this QuadTree's children.

        Args:
            direction (Direction): The direction of the quad tree to add it to.
            obj (Object): The object to add.
        """
        direction = self.determine_subtree(obj)
        if self.subtrees[direction] is None:
            self.subtrees[direction] = QuadTree(center=self.calc_new_center(direction), width=self.width/2)
        self.subtrees[direction].insert_object(obj)

    def determine_subtree(self, obj: Object) -> Direction:
        """Given an object, determine which of this QuadTree's subtrees the object should go in.

        Args:
            obj (Object): The object to add.

        Returns:
            Direction: The direction of the subtree to add this object to.
        """
        x, y = obj.get_position()
        if x <= self.center.x and y >= self.center.y:
            return Direction.NW
        if x > self.center.x and y >= self.center.y:
            return Direction.NE
        if x <= self.center.x and y < self.center.y:
            return Direction.SW
        if x > self.center.x and y < self.center.y:
            return Direction.SE

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
