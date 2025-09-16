from gravity_sim.object import Object

class Simulation:
    def __init__(self, name: str, timestep: int, objects: list[Object], description: str = None):
        self.name = name
        self.timestep = timestep
        self.objects = objects
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
            description=dictionary.get("description")
        )

    def setup():
        pass

    def step():
        pass

    def is_running() -> bool:
        pass
