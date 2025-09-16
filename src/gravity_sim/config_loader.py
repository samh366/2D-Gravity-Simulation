import random
import re
from dataclasses import dataclass, field
from gravity_sim.vector import Vector

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
    position: Vector = field(default_factory=Vector)
    velocity: Vector = field(default_factory=Vector)
    color: Color = field(default_factory=Color.random_colour)
    satellites: list["Object"]  = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        """Return an object from the provided data."""
        return cls(
            name=data["name"],
            mass=data["mass"],
            radius=data["radius"],
            position=Vector(data["position"]),
            velocity=Vector(data["velocity"]),
            color=Color.from_iterable(data.get("color")),
            satellites=[cls.from_dict(obj) for obj in data.get("satellites", [])]
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
