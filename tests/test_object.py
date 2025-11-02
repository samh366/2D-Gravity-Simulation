from gravity_sim.object import Object
from pytest import raises


class TestObject:
    """Tests the Object class."""

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
        actual_objects = Object.from_dict(dict_object)
        assert isinstance(actual_objects, list)
        assert len(actual_objects) == 2
        earth = actual_objects[0]
        moon = actual_objects[1]

        assert earth.name == dict_object["name"]
        assert earth.mass == dict_object["mass"]
        assert tuple(earth.position) == tuple(dict_object["position"])
        assert tuple(earth.velocity) == tuple(dict_object["velocity"])
        assert tuple(earth.color) == tuple(dict_object["color"])

        satellite_dict = dict_object["satellites"][0]
        assert moon.name == satellite_dict["name"]
        assert moon.mass == satellite_dict["mass"]
        assert tuple(moon.position) == (1500, -2000)
        assert tuple(moon.velocity) == (5.1, 305)
        assert tuple(moon.color) == tuple(satellite_dict["color"])
