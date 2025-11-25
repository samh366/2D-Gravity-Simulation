import math
from decimal import Decimal
from random import Random
from typing import List

from gravity_sim.object import Object
from gravity_sim.vector import Vector
from gravity_sim.quadtree import QuadTree
from collections import deque


class Simulation:
    """Class to simulate some gravitational bodies."""

    def __init__(
        self,
        name: str,
        timestep: int,
        steps: int,
        objects: list[Object],
        grav_constant: float = 6.6743e-11,
        description: str = None,
    ):
        """Create a new simulation.

        Args:
            name (str): Name of the simulation.
            timestep (int): The time to advance forward each frame.
            steps (int): The number of times to subdivide calculations in each timestep.
            objects (list[Object]): The objects in the simulation.
            grav_constant (float, optional): The gravitational constant value to use.. Defaults to 6.6743e-11.
            description (str, optional): A short description. Defaults to None.
        """
        self.name = name
        self.timestep = Decimal(timestep)
        self.steps = steps
        self.grav_constant = Decimal(grav_constant)
        self.description = description
        self.objects = objects

        self.theta = 0.5

        if self.description is None:
            self.description = "A simulation."

        self.last_quadtree = None

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
            Simulation: A loaded Simulation ready to start.
        """
        if "name" not in dictionary:
            raise ValueError("'name' field must be in config file.")

        if "timestep" not in dictionary:
            raise ValueError("'timestep' field must be in config file.")

        if len(dictionary.get("objects", [])) == 0:
            raise ValueError("'Config file contains no objects.")

        objects = []
        for obj in dictionary["objects"]:
            entity = Object.from_dict(obj)
            objects.extend(entity.get_satellites())

        return cls(
            name=dictionary["name"],
            timestep=dictionary["timestep"],
            steps=dictionary.get("steps", 1),
            objects=objects,
            description=dictionary.get("description"),
        )

    def get_random(self) -> Random:
        """Get the simulation's random number generator."""
        return self._random

    def calculate_forces(self) -> None:
        """Compute the forces between all the objects in the simulation. O(n^2)."""
        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1 is not obj2:
                    self.calculate_force_on_object(obj1, obj2.position, obj2.mass)

    def calc_forces_barnes_hut(self) -> None:
        """Calculate the forces between all objects using the Barnes-Hut algorithm. O(nlogn)."""
        if len(self.objects) < 2:
            return
        tree = self.build_quad_tree()

        for obj in self.objects:
            stack = deque([tree])
            while stack:
                node: QuadTree = stack.pop()
                if node.value is obj:
                    continue
                elif isinstance(node.value, Object):
                    self.calculate_force_on_object(obj, node.value.position, node.value.mass)
                else:
                    # Check if node is sufficiently far away such that we can approximate its mass
                    distance = obj.position.distance(node.center_of_mass)
                    distance = max(distance, 1)
                    if (node.width * 2 / distance) < self.theta:
                        self.calculate_force_on_object(obj, node.center_of_mass, node.mass)
                    else:
                        # Not far away enough, explore subtrees
                        for subtree in node.subtrees.values():
                            if subtree:
                                stack.append(subtree)

        self.last_quadtree = tree

    def build_quad_tree(self) -> QuadTree:
        """Construct a QuadTree from the objects in the Simulation.

        Returns:
            QuadTree: The created QuadTree
        """
        tree = QuadTree(center=Vector(0, 0), width=self.find_quad_tree_width())
        for obj in self.objects:
            tree.insert_object(obj)
        return tree

    def find_quad_tree_width(self) -> Decimal:
        """Find the maximum distance in one dimension between two objects in the simulation.

        Returns:
            Decimal: The width that QuadTree should be.
        """
        max_x = float("-inf")
        min_x = float("inf")
        for obj in self.objects:
            max_x = max(max_x, obj.position.x)
            min_x = min(min_x, obj.position.x)

        max_y = float("-inf")
        min_y = float("inf")
        for obj in self.objects:
            max_y = max(max_y, obj.position.y)
            min_y = min(min_y, obj.position.y)

        return max(max_x - min_x, max_y - min_y)

    def calculate_force_on_object(self, obj1: Object, obj2_pos: Vector, obj2_mass: Decimal) -> None:
        """Calculate the gravitational force applied to an object.

        Args:
            obj1 (Object): The object the force is applied to.
            obj2_pos (Vector): The position of the other object.
            obj2_mass (Decimal): The mass of the other object.
        """
        distance = obj2_pos - obj1.position
        sqrDistance = distance[0] ** 2 + distance[1] ** 2
        if math.isclose(sqrDistance, 0, rel_tol=1e-7):
            return

        force = self.grav_constant * obj1.mass * obj2_mass / sqrDistance
        theta = math.atan2(distance[1], distance[0])  # Calculate angle the force acts at
        force_vector = Vector.from_magnitude_theta(magnitude=force, theta=theta)

        obj1.add_force(force_vector)

    def move_objects(self, timestep: Decimal) -> None:
        """Move the objects in the simulation based on the forces acting on them.

        Args:
            timestep (Decimal): The timestep to move the simulation forward.
        """
        for obj in self.objects:
            obj.step(timestep)
            obj.reset_force()

    def step(self):
        """Step forward the simulation by one timestep."""
        timestep = Decimal(self.timestep / self.steps)
        for _ in range(self.steps):
            # self.calculate_forces() # Old method
            self.calc_forces_barnes_hut()
            self.move_objects(timestep)

    def run(self):
        """Run the simulation."""
        while True:
            self.step()

    def get_objects(self) -> List[Object]:
        """Return a list of all objects in the simulation.

        Returns:
            List[Object]: A list of objects in the simulation.
        """
        return self.objects

    def get_num_objects(self) -> int:
        """Get the number of objects in the simulation.

        Returns:
            int: The number of objects in the simulation.
        """
        return len(self.objects)

    def get_object(self, index: int) -> Object:
        """Get an object at a certain index.

        Args:
            index (int): Index of the object to get.

        Returns:
            Object: THe object at the given index
        """
        try:
            return self.objects[index]
        except IndexError:
            raise IndexError(f"Index {index} out of bounds for {len(self.objects)} objects in simulation.")

    def get_timestep(self) -> Decimal:
        """Get the current timestep.

        Returns:
            Decimal: The current timestep.
        """
        return self.timestep

    def set_timestep(self, new_timestep: Decimal) -> None:
        """Set the current timestep.

        Args:
            new_timestep (Decimal): The new timestep.
        """
        self.timestep = new_timestep
