import re
from gravity_sim.simulation import Simulation
from yaml import CSafeLoader, load
from collections import deque
from gravity_sim.random_factory import RandomFactory
from random import Random
from typing import Union
from decimal import Decimal


class YamlParser:
    """Class to convert random parameters in simulation config to values."""

    def __init__(self, rng: Random):
        """Create a new YAML parser with a random number generator.

        Args:
            rng (Random): The random number generator to use for random calculations.
        """
        self._rng = rng

    def parse(self, config: dict) -> dict:
        """Parse all random parameters and resolve them to actual values.

        Args:
            config (dict): A simulation config.

        Returns:
            dict: The config update in-place.
        """
        queue = deque()
        for obj in config["objects"]:
            queue.append(obj)
        while queue:
            obj = queue.popleft()
            for sat in obj.get("satellites", []):
                queue.append(sat)
            self.resolve_random_values(obj)
        return config

    def resolve_random_values(self, obj: dict) -> None:
        """Convert any random parameters to values in the provided dictionary in-place.

        Args:
            obj (dict): A dictionary representation of an object.
        """
        if isinstance(obj["mass"], dict):
            obj["mass"] = self.random_int(obj["mass"])
        if isinstance(obj["position"], dict):
            obj["position"] = self.random_vector(obj["position"])
        if isinstance(obj["velocity"], dict):
            obj["velocity"] = self.random_vector(obj["velocity"])

    def _check_random_parameters(self, values: dict):
        """Raise an error if the arguments "min" and "max" are not in the provided dict.

        Args:
            values (dict): The dictionary to check;
        """
        if "max" not in values:
            raise ValueError("'max' value not found when creating random value.")
        if "min" not in values:
            raise ValueError("'min' value not found when creating random value.")

    @staticmethod
    def parse_number(number: Union[int, float, str, Decimal]) -> int:
        """Convert a float, int or string scientific number to an accurate integer.

        Args:
            number (Union[int, float, str, Decimal]): Some int, float, string or Decimal.

        Returns:
            int: The number as an integer.
        """
        return int(Decimal(number))

    @staticmethod
    def parse_number_list(number_list: list[Union[int, float, str, Decimal]]) -> list[int]:
        """Convert some iterable of floats, ints, strings or decimals to a list of integers.

        Args:
            number_list (list[Union[int, float, str, Decimal]]): Some list of values.

        Returns:
            list[int]: The list of values as integers.
        """
        return [int(Decimal(num)) for num in number_list]

    def random_vector(self, values: dict) -> list[int]:
        """Return a random vector in list form.

        Args:
            values (dict): A dictionary containing max and min values for the vector.

        Returns:
            list[int]: A random vector as a list of integers.
        """
        self._check_random_parameters(values)
        max_values = YamlParser.parse_number_list(values["max"])
        min_values = YamlParser.parse_number_list(values["min"])
        return [self._rng.randint(min_values[0], max_values[0]), self._rng.randint(min_values[1], max_values[1])]

    def random_int(self, values) -> int:
        """Generate a random integer.

        Args:
            values (dict): A dictionary containing the max and min values.

        Returns:
            _type_: A random integer in the given bounds.
        """
        self._check_random_parameters(values)
        max_val = YamlParser.parse_number(values["max"])
        min_val = YamlParser.parse_number(values["min"])
        return self._rng.randint(max_val, min_val)


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

        raise ValueError(f"Unable to load data from {filename}: File should be .y(a)ml.")

    @staticmethod
    def from_yaml(filename: str) -> Simulation:
        """Load data from a YAML file into a Simulation object."""
        with open(filename, "r") as yaml_file:
            data = load(yaml_file, Loader=CSafeLoader)
        RandomFactory.set_random(data.get("seed", None))
        parser = YamlParser(RandomFactory.get_random())
        return Simulation.from_dict(parser.parse(data))
