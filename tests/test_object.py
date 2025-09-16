from gravity_sim.config_loader import Object
from pytest import raises


class TestObject:
    """Tests the Object class."""
    def test_from_dict_with_satellite(self):
        """An object with correct data should be returned when given a dictionary."""
        dict_object = {
            "name": "Earth",
            "mass": 5.972e24,
            "radius": 6371,
            "position": [149597870.7, 0],
            "velocity": [0, 29780],
            "color": [0, 100, 255],
            "satellites": [
                {
                    "name": "Moon",
                    "mass": 5.972e24,
                    "radius": 6371,
                    "position": [149597870.7, 0],
                    "velocity": [0, 29780],
                    "color": [0, 100, 255]
                }
            ]
        }
        actual_object = Object.from_dict(dict_object)
        assert isinstance(actual_object, Object)

        assert actual_object.name == dict_object["name"]
        assert actual_object.mass == dict_object["mass"]
        assert actual_object.radius == dict_object["radius"]
        assert tuple(actual_object.position) == tuple(dict_object["position"])
        assert tuple(actual_object.velocity) == tuple(dict_object["velocity"])
        assert tuple(actual_object.color) == tuple(dict_object["color"])

        assert len(actual_object.satellites) == len(dict_object["satellites"])
        satellite = actual_object.satellites[0]
        satellite_dict = dict_object["satellites"][0]
        assert satellite.name == satellite_dict["name"]
        assert satellite.mass == satellite_dict["mass"]
        assert satellite.radius == satellite_dict["radius"]
        assert tuple(satellite.position) == tuple(satellite_dict["position"])
        assert tuple(satellite.velocity) == tuple(satellite_dict["velocity"])
        assert tuple(satellite.color) == tuple(satellite_dict["color"])

