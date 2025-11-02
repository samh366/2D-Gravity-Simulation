import pytest

from gravity_sim.object import Object
from gravity_sim.vector import Vector


class TestObject:
    """Tests the Object class."""

    @pytest.fixture
    def obj(self) -> Object:
        """Fixture to create an example object."""
        return Object.from_dict(
            {
                "name": "Earth",
                "mass": 5.972e24,
                "position": [1000, -1000],
                "velocity": [10.1, 100],
                "color": [0, 100, 255],
                "satellites": [
                    {
                        "name": "Moon",
                        "mass": 5972,
                        "position": [500, -1000],
                        "velocity": [-5, 205],
                        "color": [255, 100, 255],
                    }
                ],
            }
        )

    def test_from_dict_with_satellite(self):
        """An object with a satellite should be returned correctly.

        A list should be returned containing the object and it's satellites.
        All positions and velocities should be relative to a parent objects'.
        """
        dict_object = {
            "name": "Earth",
            "mass": 5.972e24,
            "position": [1000, -1000],
            "velocity": [10.1, 100],
            "color": [0, 100, 255],
            "satellites": [
                {
                    "name": "Moon",
                    "mass": 5972,
                    "position": [500, -1000],
                    "velocity": [-5, 205],
                    "color": [255, 100, 255],
                }
            ],
        }
        earth = Object.from_dict(dict_object)
        assert isinstance(earth, Object)

        assert earth.name == dict_object["name"]
        assert earth.mass == dict_object["mass"]
        assert earth.position.to_tuple() == tuple(dict_object["position"])
        assert earth.velocity.to_tuple() == tuple(dict_object["velocity"])
        assert tuple(earth.color) == tuple(dict_object["color"])

        assert len(earth.satellites) == 1
        moon = earth.satellites[0]

        satellite_dict = dict_object["satellites"][0]
        assert moon.name == satellite_dict["name"]
        assert moon.mass == satellite_dict["mass"]
        assert moon.position.to_tuple() == (1500, -2000)
        assert moon.velocity.to_tuple() == (5.1, 305)
        assert tuple(moon.color) == tuple(satellite_dict["color"])

    def test_add_force(self, obj: Object):
        """add_force should add a force to the object."""
        obj.force = Vector()
        obj.add_force(Vector(2, 5))

        assert obj.force[0] == 2
        assert obj.force[1] == 5

    def test_reset_force(self, obj: Object):
        """reset_force should reset an object's force to 0, 0."""
        obj.force = Vector(2, 5)
        obj.reset_force()

        assert obj.force[0] == 0
        assert obj.force[1] == 0

    def test_get_position(self, obj: Object):
        """get_position should return the correct position."""
        obj.position = Vector(1, 2)
        result = obj.get_position()

        assert result[0] == 1
        assert result[1] == 2

    def test_get_satellites(self, obj: Object):
        """get_satellites should return a list containing this object and all satelites."""
        moon = obj.satellites[0]

        satellites = obj.get_satellites()

        assert isinstance(satellites, list)
        assert len(satellites) == 2
        assert satellites[0] is obj
        assert satellites[1] is moon
