from gravity_sim.config_loader import YamlParser
from random import Random


class TestYamlParser:
    """Test YamlParser class."""

    def test_random_int(self):
        """A random integer should be generated in a given range."""
        parser = YamlParser(Random(1))
        values = {"max": 1, "min": 0}
        result = parser.random_int(values)

        assert result == 1 or result == 0

    def test_random_int_scientific(self):
        """A random integer should be generated in a given range."""
        parser = YamlParser(Random(1))
        values = {"max": 2e5, "min": 2e4}
        result = parser.random_int(values)

        assert result <= 2e5 and result >= 2e4

    def test_random_vector(self):
        """A random integer should be generated in a given range."""
        parser = YamlParser(Random(2))
        values = {"max": [1, 3], "min": [0, 2]}
        result = parser.random_vector(values)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == 1 or result[0] == 0
        assert result[1] == 2 or result[1] == 3

    def test_resolve_random_values_int(self):
        """Random values should be replaced with actual values."""
        parser = YamlParser(Random(3))
        data = {
            "name": "Earth",
            "mass": {"max": 2, "min": 1},
            "position": [1, 1],
            "velocity": [0, 29_780],
            "color": [0, 100, 255],
        }

        parser.resolve_random_values(data)

        assert isinstance(data["mass"], int)
        assert data["mass"] == 1 or data["mass"] == 2

    def test_resolve_random_values_vector(self):
        """Random values should be replaced with actual values."""
        parser = YamlParser(Random(3))
        data = {
            "name": "Earth",
            "mass": 5.972e24,
            "position": {
                "max": [0, 2],
                "min": [-1, 2],
            },
            "velocity": [0, 29_780],
            "color": [0, 100, 255],
        }

        parser.resolve_random_values(data)

        assert isinstance(data["position"], list)
        assert len(data["position"]) == 2

        assert isinstance(data["position"][0], int)
        assert isinstance(data["position"][1], int)

        assert data["position"][0] == 0 or data["position"] == -1
        assert data["position"][1] == 2

    def test_resolve_random_values_multiple(self):
        """Random values should be replaced with actual values."""
        parser = YamlParser(Random(3))
        data = {
            "name": "Earth",
            "mass": {"min": 6, "max": 7},
            "position": {
                "max": [0, 2],
                "min": [-1, 2],
            },
            "velocity": {
                "max": [1, 5],
                "min": [0, 3],
            },
            "color": [0, 100, 255],
        }

        parser.resolve_random_values(data)

        # Check mass
        assert isinstance(data["mass"], int)
        assert data["mass"] == 7 or data["mass"] == 6
        # Check position
        assert isinstance(data["position"], list)
        assert len(data["position"]) == 2
        assert isinstance(data["position"][0], int)
        assert isinstance(data["position"][1], int)
        # Check velocity
        assert isinstance(data["velocity"], list)
        assert len(data["velocity"]) == 2
        assert isinstance(data["velocity"][0], int)
        assert isinstance(data["velocity"][1], int)

    def test_resolve_random_values_no_changes(self):
        """No changes should be made when there are no random parameters."""
        parser = YamlParser(Random(3))
        data = {
            "name": "Earth",
            "mass": 100,
            "position": [10, 5],
            "velocity": [2, 3],
            "color": [0, 100, 255],
        }

        parser.resolve_random_values(data)

        # Check mass
        assert isinstance(data["mass"], int)
        assert data["mass"] == 100
        # Check position
        assert isinstance(data["position"], list)
        assert len(data["position"]) == 2
        assert isinstance(data["position"][0], int)
        assert isinstance(data["position"][1], int)
        assert data["position"][0] == 10
        assert data["position"][1] == 5
        # Check velocity
        assert isinstance(data["velocity"], list)
        assert len(data["velocity"]) == 2
        assert isinstance(data["velocity"][0], int)
        assert isinstance(data["velocity"][1], int)
        assert data["velocity"][0] == 2
        assert data["velocity"][1] == 3
