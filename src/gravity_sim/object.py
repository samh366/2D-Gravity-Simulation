from dataclasses import dataclass, field
import random
from gravity_sim.vector import Vector
from typing import List


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
        return str(tuple(self))


@dataclass
class Object:
    """Represents an object in a simulation."""

    name: str
    mass: int
    position: Vector = field(default_factory=Vector)
    velocity: Vector = field(default_factory=Vector)
    color: Color = field(default_factory=Color.random_colour)
    satellite_data: list[dict] = field(default_factory=list)

    force: Vector = field(default_factory=Vector)

    def __post_init__(self):
        """Initialise satellites."""
        self.satellites = []
        for obj in self.satellite_data:
            self.satellites.append(self.__class__.from_dict(obj, rel_pos=self.position, rel_vel=self.velocity))

    @classmethod
    def from_dict(
        cls, data: dict, rel_pos: Vector = None, rel_vel: Vector = None, rng: random.Random = None
    ) -> "Object":
        """Return an object from a dictionary.

        Args:
            data (dict): Dictionary containing object information.
            rel_pos (Vector): The position of the parent object.
            rel_vel (Vector): The velocity of the parent object.

        Raises:
            ValueError: If any values in data or invalid.

        Returns:
            List[Object]: An object and any child objects flattened out.
        """
        if rel_pos is None:
            rel_pos = Vector(0, 0)
        if rel_vel is None:
            rel_vel = Vector(0, 0)
        if rng is None:
            rng = random
        try:
            mass = cls.random_int(data["mass"], rng)
        except ValueError as e:
            raise ValueError(f"Error trying to load mass value {data['mass']}: {e}")

        position = cls.random_vector(data["position"], rng) + rel_pos
        velocity = cls.random_vector(data["velocity"], rng) + rel_vel

        loaded_object = cls(
            name=data["name"],
            mass=mass,
            position=position,
            velocity=velocity,
            color=Color.from_iterable(data.get("color")),
            satellite_data=data.get("satellites", []),
        )

        return loaded_object

    @classmethod
    def random_vector(self, val: dict[list[int | str]], rng: random.Random):
        if isinstance(val, list):
            return Vector(*list(map(float, val)))

        if not isinstance(val, dict):
            raise ValueError(f"Invalid type {val.__class__}")

        if not val.get("min") or not val.get("max"):
            raise ValueError("Invalid keys, random dict must contain 'min' and 'max' values.")

        if len(val["min"]) != len(val["max"]):
            raise ValueError("Min and max lists have mismatched lengths.")

        values = []
        for min, max in zip(val["min"], val["max"]):
            min = int(float(min))
            max = int(float(max))
            values.append(rng.randint(min, max))

        return Vector(*values)

    @classmethod
    def random_int(self, val: int | str | dict, rng: random.Random):
        """If val contains min and max values, generate a random int, else return val.

        Args:
            val (int | str | dict): A float or a dictionary containing the keys 'min' and 'max'.
        """
        try:
            if isinstance(val, (int, str)):
                return int(float(val))
        except ValueError:
            raise ValueError("Integer value required.")

        if not isinstance(val, dict):
            raise ValueError(f"Invalid type {val.__class__}")

        if not val.get("min") or not val.get("max"):
            raise ValueError("Invalid keys, random dict must contain 'min' and 'max' values.")

        min = int(float(val.get("min")))
        max = int(float(val.get("max")))
        return rng.randint(min, max)

    def add_force(self, force: Vector) -> None:
        """Add an external force to the force this object is experiencing.

        Args:
            force (Vector): An external force acting on the object.
        """
        self.force += force

    def reset_force(self) -> None:
        """Reset force vector to zero."""
        self.force = Vector()

    def get_position(self) -> Vector:
        """Return the current position."""
        return self.position

    def get_satellites(self) -> list["Object"]:
        """Recursively get all satellites of this object."""
        # TODO: Implement
        return []

    def step(self, timestep: float) -> None:
        """Recalculate position based on current force value and timestep.

        Args:
            timestep (float): Time passed in seconds.
        """
        self.velocity += self.force / self.mass * timestep
        self.position += self.velocity * timestep
