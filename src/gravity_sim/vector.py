class Vector:
    """A Vector class."""

    def __init__(self, x: float, y: float):
        """Initialise a vector given an x and y value."""
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        """Check equality between this vector and another object.

        Args:
            other (object): The object to check equality against.

        Returns:
            bool: True if equal, False otherwise.
        """
        if not isinstance(object, Vector):
            return False
        if other.x != self.x:
            return False
        if other.y != self.y:
            return False
        return True
