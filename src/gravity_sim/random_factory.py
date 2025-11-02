from random import Random
from typing import Optional


class RandomFactory:
    """Singleton class to store the random number generator."""

    _random = None

    def __init__(self):
        """Init, do not use."""
        raise RuntimeError("Call set_random() or get_random() instead!")

    @classmethod
    def get_random(cls) -> Random:
        """Get the random number generator. Must call set_random() first.

        Raises:
            RuntimeError: If set_random() has not been called first.

        Returns:
            Random: The current random number generator.
        """
        if cls._random is None:
            raise RuntimeError("Call set_random() first!")
        return cls._random

    @classmethod
    def set_random(cls, seed: Optional[int]) -> None:
        """Set the random number generator given a seed.

        Args:
            seed (Optional[int]): The seed to use, can be None for a random value.
        """
        if not cls._random:
            cls._random = Random(seed)
