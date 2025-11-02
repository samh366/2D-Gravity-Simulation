from pytest import mark, raises

from gravity_sim.object import Color


class TestColor:
    """Test the Color class."""

    def test_init(self):
        """Init should correctly create a color object."""
        color = Color(10, 20, 30)
        assert color.r == 10
        assert color.g == 20
        assert color.b == 30

    def test_iter(self):
        """__iter__ should correctly iterate through the color object."""
        color = Color(1, 2, 3)
        assert list(color) == [1, 2, 3]

    @mark.parametrize(
        "color, id, expected",
        [
            (Color(5, 6, 7), 0, 5),
            (Color(5, 6, 7), 1, 6),
            (Color(5, 6, 7), 2, 7),
        ],
    )
    def test_getitem(self, color, id, expected):
        """Getting an item should return the correct item."""
        assert color[id] == expected

    def test_getitem_out_of_range(self):
        """Getting an item out of range should raise an IndexError."""
        color = Color(1, 2, 3)
        with raises(IndexError):
            _ = color[3]

    def test_random_colour_range(self):
        """Random colours should have rgb values between 50 and 200."""
        color = Color.random_colour()
        assert 50 <= color.r <= 200
        assert 50 <= color.g <= 200
        assert 50 <= color.b <= 200

    @mark.parametrize(
        "input_val, expected",
        [
            ((10, 20, 30), (10, 20, 30)),
            ([255, 0, 128], (255, 0, 128)),
            ((-10, 300, 128), (0, 255, 128)),
            ((1.9, 2.1, 3.7), (2, 2, 4)),
        ],
    )
    def test_from_iterable(self, input_val, expected):
        """From iterable should correctly instantiate a color object."""
        color = Color.from_iterable(input_val)
        assert (color.r, color.g, color.b) == expected

    def test_from_iterable_none(self):
        """From iterable with None should create a random color."""
        color = Color.from_iterable(None)
        assert 50 <= color.r <= 200
        assert 50 <= color.g <= 200
        assert 50 <= color.b <= 200

    def test_from_iterable_non_iterable(self):
        """Calling from_iterable with a non-iterable should raise an error."""
        with raises(ValueError):
            Color.from_iterable(123)

    def test_str(self):
        """String representation should be accurate."""
        color = Color(1, 2, 3)
        assert str(color) == "(1, 2, 3)"
