import random
import re
from dataclasses import dataclass, field
from gravity_sim.vector import Vector
from gravity_sim.simulation import Simulation
from yaml import CSafeLoader, load

@dataclass
class Color:
    """Stores an RGB color."""
    r: int
    g: int
    b: int

    def __iter__(self):
        """Iterate through the values in the colour."""
        return [self.r, self.g, self.b].__iter__()

    def __getitem__(self, key):
        """Return the requested item."""
        match key:
            case 0:
                return self.r
            case 1:
                return self.g
            case 2:
                return self.b
        raise IndexError(f"Color object does not have index {key}!")

    @classmethod
    def random_colour(cls) -> "Color":
        """Return a random color object.

        Returns:
            Color: A color object with random RGB values between 50 and 200.
        """
        return cls(
            r=random.randint(50, 200),
            g=random.randint(50, 200),
            b=random.randint(50, 200),
        )

    @classmethod
    def from_iterable(cls, iterable: object) -> "Color":
        """Return a color object from an iterable of 3 integers.

        Args:
            iterable (object): Some iterable in the format (R, G, B)

        Returns:
            Color: A Color object of the provided color.
        """
        if iterable is None:
            return cls.random_colour()

        if not hasattr(iterable, "__iter__"):
            raise ValueError(f"Object {iterable} does not have attribute __iter__.")

        def format(num: int):
            """Bound a number between 0 and 255, and round it to an integer."""
            return min(255, max(0, round(num)))

        return cls(
            format(iterable[0]),
            format(iterable[1]),
            format(iterable[2]),
        )

    def __str__(self) -> str:
        """Return a string representation of the color."""
        return str(self.as_tuple())

class ConfigLoader:
    """Loads simulation configs from various types of config files."""

    @staticmethod
    def load_file(filename: str) -> Simulation:
        """Return a simulation object loaded from the data in the given file.

        Args:
            filename (str): The filename, should end in .yaml or .yml.

        Returns:
            Simulation: A Simulation object with the loaded data.
        """
        if re.search(r".*\.ya?ml", filename):
            return ConfigLoader.from_yaml(filename)

        raise ValueError(f"Unable to load data from {filename}: File should be .yaml.")

    @staticmethod
    def from_yaml(filename: str) -> Simulation:
        """Load data from a YAML file into a Simulation object."""
        with open(filename, "r") as yaml_file:
            data = load(yaml_file, Loader=CSafeLoader)
        return Simulation.from_dict(data)

    @staticmethod
    def from_json() -> Simulation:
        pass
