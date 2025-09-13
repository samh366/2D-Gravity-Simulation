from gravity_sim.config_loader import Object
from pytest import raises


class TestObject:
    """Tests the Object class."""
    def test_from_dict(self):
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
        
        expected_object = Object(
            
        )

