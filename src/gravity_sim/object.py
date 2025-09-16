from dataclasses import dataclass, field
from gravity_sim.vector import Vector
from gravity_sim.config_loader import Color


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
