from random import Random

from pytest import raises

from gravity_sim.random_factory import RandomFactory


class TestRandomFactory:
    """Test the vector class."""

    def test_init(self):
        """Calling init of RandomFactory should raise an error."""
        with raises(RuntimeError):
            RandomFactory()

    def test_set_random(self):
        """Calling set random should set the random number generator."""
        RandomFactory._random = None
        RandomFactory.set_random(1)

        assert isinstance(RandomFactory._random, Random)

    def test_get_random(self):
        """Calling get_random should return the set random number generator."""
        RandomFactory._random = Random(1)

        assert isinstance(RandomFactory.get_random(), Random)
