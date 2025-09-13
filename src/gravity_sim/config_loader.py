import random
import re
from dataclasses import dataclass, field

@dataclass
class Color:
    """Stores an RGB color."""
    r: int
    g: int
    b: int

    @classmethod
    def from_iterable(cls, iterable: object) -> "Color":
        """Return a color object from an iterable of 3 integers.

        Args:
            iterable (object): Some iterable in the format (R, G, B)

        Returns:
            Color: A Color object of the provided color.
        """

        def format(num: int):
            """Bound a number between 0 and 255, and round it to an integer."""
            return min(255, min(0, round(num)))

        return cls(
            format(iterable[0]),
            format(iterable[1]),
            format(iterable[2]),
        )

    def as_tuple(self) -> tuple:
        """Return the color as an RGB tuple."""
        return (self.r, self.g, self.b)

    def __str__(self) -> str:
        """Return a string representation of the color."""
        return str(self.as_tuple())

def random_colour() -> Color:
    """Return a random color.

    Returns:
        Color: A color object with random RGB values between 50 and 200.
    """
    return Color(
        r=random.randint(50, 200),
        g=random.randint(50, 200),
        b=random.randint(50, 200),
    )

dict_object = {
    "name": "Earth",
    "mass": 5.972e24,
    "radius": 6371,
    "position": [149597870.7, 0],
    "velocity": [0, 29780],
    "color": [0, 100, 255],
    "satellites": [
        {
            "name": "Moon",
            "mass": 5.972e24,
            "radius": 6371,
            "position": [149597870.7, 0],
            "velocity": [0, 29780],
            "color": [0, 100, 255]
        }
    ]
}

@dataclass
class Object:
    """Represents an object in a simulation."""
    name: str
    mass: int
    radius: int
    position: list[float] = field(default_factory=list[float])
    velocity: list[float] = field(default_factory=list[float])
    color: Color = field(default_factory=random_colour)
    satellites: list["Object"]  = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        """Create an object from a dictionary representation."""

        return cls(
            name=data["name"],
            satellites = [cls.from_dict(obj) for obj in data["satellites"]]
        )


@dataclass
class Config:
    """Dataclass to store the starting config of a simulation."""

    @classmethod
    def from_dict():
        """Loads a config"""


class ConfigLoader:
    """Loads simulation configs from various types of config files."""

    @staticmethod
    def load_file(filename: str) -> Config:
        if re.search(".*.y*ml", filename):
            return ConfigLoader.from_yaml(filename)

    @staticmethod
    def from_yaml(filename: str):
        pass

    @staticmethod
    def from_json() -> Config:
        pass
