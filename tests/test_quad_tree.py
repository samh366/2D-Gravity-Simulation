from decimal import Decimal

import pytest

from gravity_sim.object import Object
from gravity_sim.quadtree import QuadTree
from gravity_sim.vector import Vector
from gravity_sim.quadtree import Direction


class TestQuadTree:
    """Tests the Object class."""

    @pytest.fixture
    def obj(self) -> Object:
        """Fixture to create an example object."""
        return Object.from_dict(
            {
                "name": "Earth",
                "mass": 5.972e24,
                "position": [1, 1],
                "velocity": [1, 1],
                "color": [0, 100, 255],
            }
        )

    @pytest.fixture
    def obj2(self) -> Object:
        """Fixture to create second different example object."""
        return Object.from_dict(
            {
                "name": "Mars",
                "mass": 5.972e23,
                "position": [6, 6],
                "velocity": [1, 1],
                "color": [255, 50, 50],
            }
        )

    def test_empty_quad_tree(self):
        """Initialising a new quad tree should create a Quad Tree with 4 children set to None."""
        tree = QuadTree(center=Vector(100, -100), width=50)

        assert tree.mass == 0
        assert tree.value is None
        assert tree.width == Decimal(50)
        for val in tree.subtrees.values():
            assert val is None

    @pytest.mark.parametrize(
        "direction, width, expected",
        [
            pytest.param(Direction.NW, 100, Vector(-50, 50)),
            pytest.param(Direction.NE, 100, Vector(50, 50)),
            pytest.param(Direction.SW, 100, Vector(-50, -50)),
            pytest.param(Direction.SE, 100, Vector(50, -50)),
            pytest.param(Direction.SE, 25, Vector(12.5, -12.5)),
        ],
        ids=["North west", "North east", "South west", "South east", "Floating point"],
    )
    def test_calc_new_center(self, direction: Direction, width: int, expected: Vector):
        """New centers should be calculated correctly given the direction."""
        tree = QuadTree(center=Vector(0, 0), width=width)
        actual = tree.calc_new_center(direction)

        assert actual == expected

    def test_add_to_lower_quad_tree(self, obj: Object):
        """Objects should be correctly added to lower quad trees."""
        tree = QuadTree(center=Vector(0, 0), width=50)
        obj.position = Vector(-20, -20)
        tree.add_to_subtree(obj)

        for key, val in tree.subtrees.items():
            if key == Direction.SW:
                assert isinstance(tree.subtrees[Direction.SW], QuadTree)
                continue
            assert val is None

        subtree = tree.subtrees[Direction.SW]
        assert subtree.value is obj
        assert subtree.mass == obj.mass

    def test_insert_object_empty(self, obj: Object):
        """Inserting an object into an empty QuadTree should just set it as the QuadTree's value."""
        tree = QuadTree(center=Vector(0, 0), width=50)
        tree.insert_object(obj)

        assert tree.value is obj
        assert tree.mass == obj.mass
        for val in tree.subtrees.values():
            assert val is None

    def test_insert_object_full(self, obj: Object, obj2: Object):
        """When a quadtree is full, the current value and the new value should both be divided among subtrees."""
        tree = QuadTree(center=Vector(0, 0), width=10)
        tree.insert_object(obj)
        tree.insert_object(obj2)

        assert tree.value is None
        assert tree.mass == obj.mass + obj2.mass
        assert tree.num_items == 2

        assert isinstance(tree.subtrees[Direction.NE], QuadTree)
        subtree = tree.subtrees[Direction.NE]
        assert isinstance(subtree.subtrees[Direction.NE], QuadTree)
        assert isinstance(subtree.subtrees[Direction.SW], QuadTree)

        subtreeNE = subtree.subtrees[Direction.NE]
        assert subtreeNE.value is obj2
        assert subtreeNE.mass == obj2.mass
        assert subtreeNE.num_items == 1

        subtreeSW = subtree.subtrees[Direction.SW]
        assert subtreeSW.value is obj
        assert subtreeSW.mass == obj.mass
        assert subtreeSW.num_items == 1
