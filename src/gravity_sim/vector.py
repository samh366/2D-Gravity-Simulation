import math

class Vector:
    """A Vector class."""

    def __init__(self, *args):
        """Initialise a vector given an x and y values."""
        if len(args) == 0:
            self.values = (0.0, 0.0)
        elif len(args) == 1 and hasattr(args[0], "__iter__"):
            self.values = tuple(args[0])
        else:
            self.values = tuple(args)

    def __iter__(self):
        """Iterate through the values in the vector."""
        return self.values.__iter__()

    def __len__(self):
        """Return the number of dimensions the vector has."""
        return len(self.values)

    def __getitem__(self, key):
        """Return the requested item."""
        return self.values[key]

    def __repr__(self):
        """Return a text representation of the vector."""
        return str(self.values)

    def __str__(self):
        """Return a string representation of the vector."""
        return f"{self.__len__()}D Vector: {self.__repr__()}"

    def __eq__(self, other: object) -> bool:
        """Check equality between this vector and another object.

        Args:
            other (object): The object to check equality against.

        Returns:
            bool: True if equal, False otherwise.
        """
        if not isinstance(other, Vector):
            return False
        equal = (math.isclose(a, b) for a, b in zip(self, other))
        return all(equal)

    def __add__(self, other) -> "Vector":
        """Add a Vector or constant to this vector.

        Args:
            other (Vector, float, int): A vector or float/int to add to this vector.

        Returns:
            Vector: A vector with the new values.
        """
        if isinstance(other, Vector):
            return Vector(*tuple(a + b for a, b in zip(self, other)))
        if isinstance(other, (float, int)):
            return Vector(*tuple(a + other for a in self))
        raise ValueError(f"Addition not supported between {self.__class__} and {other.__class__}")

    def __sub__(self, other) -> "Vector":
        """Subtract a Vector or constant from this vector.

        Args:
            other (Vector, float, int): A vector or float/int to subtract from this vector.

        Returns:
            Vector: A vector with the new values.
        """
        if isinstance(other, Vector):
            return Vector(*tuple(a - b for a, b in zip(self, other)))
        if isinstance(other, (float, int)):
            return Vector(*tuple(a - other for a in self))
        raise ValueError(f"Subtraction not supported between {self.__class__} and {other.__class__}")
