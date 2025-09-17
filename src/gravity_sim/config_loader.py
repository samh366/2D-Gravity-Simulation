import re
from gravity_sim.simulation import Simulation
from yaml import CSafeLoader, load


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
