from gravity_sim.vector import Vector
import pytest
import math


class TestVector:
    """Test the vector class."""

    def are_lists_close(self, list1, list2):
        """Return true if all the values in the two provided lists are between 1e-7."""
        if len(list1) != len(list2):
            raise ValueError(f"List {list1} and list {list2} are not the same length.")
        for a, b in zip(list1, list2):
            if not math.isclose(a, b, abs_tol=1e-7):
                return False
        return True

    def test_init_empty(self):
        """Creating a new Vector with no args should make a Vector with 0,0."""
        vector = Vector()

        assert vector.values == (0.0, 0.0)

    def test_init_5_values(self):
        """Init should accept any number of values."""
        vector = Vector(1, 2, 3, 4, 5)

        assert vector.values == (1, 2, 3, 4, 5)

    def test_init_int(self):
        """Test init with integers."""
        vector = Vector(1, 2)

        assert vector.values == (1, 2)

    def test_init_float(self):
        """Test init with floats."""
        vector = Vector(1.2, 3.4)

        assert vector.values == (1.2, 3.4)

    def test_init_negative(self):
        """Test init with negative values."""
        vector = Vector(-1, -2.3)

        assert vector.values == (-1, -2.3)

    def test_init_large(self):
        """Test with large values."""
        vector = Vector(-999999999999999999999, 999999999999999999999)

        assert vector.values == (-999999999999999999999, 999999999999999999999)

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            pytest.param(Vector(10, 7), Vector(5, 3), (15, 10)),
            pytest.param(Vector(2.1, 3.2), Vector(1.5, 6.6), (3.6, 9.8)),
            pytest.param(Vector(5, 6.5), Vector(-9, -4.4), (-4, 2.1)),
            pytest.param(Vector(5, 2.7), Vector(0, 0), (5, 2.7)),
        ],
        ids=[
            "integer addition",
            "float addition",
            "negative addition",
            "zero addition",
        ]
    )
    def test_addition(self, a: Vector, b: Vector, expected: Vector):
        """Adding two vectors should return a new vector with correct values."""
        result = a.__add__(b)
        result: Vector

        assert self.are_lists_close(result, expected)

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            pytest.param(Vector(10, 7), Vector(5, 3), (5, 4)),
            pytest.param(Vector(2.1, 3.2), Vector(1.5, 6.6), (0.6, -3.4)),
            pytest.param(Vector(5, 6.5), Vector(-9, -4.4), (14, 10.9)),
            pytest.param(Vector(5, 2.7), Vector(0, 0), (5, 2.7)),
        ],
        ids=[
            "integer subtraction",
            "float subtraction",
            "negative subtraction",
            "zero subtraction",
        ]
    )
    def test_subtraction(self, a: Vector, b: Vector, expected: Vector):
        """Subtracting two vectors should return a new vector with correct values."""
        result = a.__sub__(b)
        result: Vector

        assert self.are_lists_close(result, expected)

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            pytest.param(Vector(1, 1), Vector(1, 1), True)
        ],
        ids=[
            "Equal integers",
        ]
    )
    def test_eq(self, a: Vector, b: Vector, expected: bool):
        """Vectors with the same or close values should be equal."""
        result = a.__eq__(b)

        assert result == expected
