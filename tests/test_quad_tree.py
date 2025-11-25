from decimal import Decimal

import pytest

from gravity_sim.object import Object
from gravity_sim.quadtree import QuadTree
from gravity_sim.vector import Vector


class TestQuadTree:
    """Tests the Object class."""

    @pytest.fixture
    def obj(self) -> Object:
        """Fixture to create an example object."""
        return Object.from_dict(
            {
                "name": "Earth",
                "mass": 5.972e24,
                "position": [0, 0],
                "velocity": [1, 1],
                "color": [0, 100, 255],
            }
        )

    def test_empty_quad_tree(self):
        """Initialising a new quad tree should create a Quad Tree with 4 children set to None."""
        tree = QuadTree(center=Vector(100, -100), width=50)

        assert tree.mass == 0
        assert tree.value is None
        assert tree.width == Decimal(50)
        for key, val in tree.corners.items():
            assert val is None
