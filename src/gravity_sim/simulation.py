from gravity_sim.object import Object
from gravity_sim.vector import Vector
import math


class Simulation:
    def __init__(
        self,
        name: str,
        timestep: int,
        objects: list[Object],
        grav_constant: float = 6.6743e-11,
        description: str = None,
        render: bool = False,
    ):
        self.name = name
        self.timestep = timestep
        self.objects = objects
        self.grav_constant = grav_constant
        self.description = description

        if self.description is None:
            self.description = "A simulation."

    @classmethod
    def from_dict(cls, dictionary: dict) -> "Simulation":
        """Return a simulation object from the provided data.

        Args:
            dictionary (dict): Dictionary to load into simulation.

        Raises:
            ValueError: If 'name' field is not in dictionary.
            ValueError: If 'timestep' field is not in dictionary.
            ValueError: If 'objects' field is not in dictionary or is empty.

        Returns:
            Simulation: _description_
        """
        if "name" not in dictionary:
            raise ValueError("'name' field must be in config file.")

        if "timestep" not in dictionary:
            raise ValueError("'timestep' field must be in config file.")

        if len(dictionary.get("objects", [])) == 0:
            raise ValueError("'Config file contains no objects.")

        return cls(
            name=dictionary["name"],
            timestep=dictionary["timestep"],
            objects=dictionary["objects"],
            description=dictionary.get("description"),
        )

    def calculate_forces(self):
        """Compute the forces between all the objects in the simulation."""
        # TODO: Improve by only doing half
        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1 is not obj2:
                    self.calculate_force_between_objects(obj1, obj2)

    def calculate_force_between_objects(self, object1: Object, object2: Object) -> None:
        """Apply the gravitational force of object 2 on object1.

        Args:
            object1 (Object): Object to apply the force to.
            object2 (Object): Object creating the force.
        """
        distance = object2.position - object1.position
        sqrDistance = distance[0] ** 2 + distance[1] ** 2
        if math.isclose(sqrDistance, 0, rel_tol=1e-7):
            return

        force = self.grav_constant * object1.mass * object2.mass / sqrDistance
        theta = math.atan2(distance[1], distance[0])  # Calculate angle the force acts at
        force_vector = Vector.from_magnitude_theta(magnitude=force, theta=theta)

        object1.add_force(force_vector)

    def move_objects(self) -> None:
        """Move the objects in the simulation based on the forces acting on them."""
        for obj in self.objects:
            obj.step(self.timestep)
            obj.reset_force()

    def step(self):
        """Step forward the simulation by one timstep."""
        self.calculate_forces()
        self.move_objects()

    def run(self):
        """Run the simulation."""
        while True:
            self.step()

    def is_running() -> bool:
        pass
