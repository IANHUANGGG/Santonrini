"""Unit tests for the Rulechecker Component."""
import unittest
from santorini.common.building import Building


class TestBuilding(unittest.TestCase):
    """Building test Class."""

    def test_create_building(self):
        """Test building creation."""
        building = Building()
        self.assertEqual(building.floor, 0)

    def test_building_height(self):
        """Test building floors."""
        building = Building()
        building.build()
        self.assertEqual(building.floor, 1)
        building.build()
        self.assertEqual(building.floor, 2)
        building.build()
        self.assertEqual(building.floor, 3)
        building.build()
        self.assertEqual(building.floor, 4)

    def test_building_overflow(self):
        """Test building overflow floors."""
        building = Building()
        building.build()
        building.build()
        building.build()
        building.build()
        with self.assertRaises(OverflowError) as context:
            building.build()
        self.assertTrue("Cannot build over " in str(context.exception))
