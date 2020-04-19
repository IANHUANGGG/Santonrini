"""Unit tests for the Worker Component."""
import unittest
from santorini.common.worker import Worker


class TestWorker(unittest.TestCase):
    """Worker test Class."""

    def test_create_worker(self):
        """Test worker creation"""
        worker1 = Worker("player1", 1)
        self.assertEqual(worker1.player, "player1")
        self.assertEqual(worker1.number, 1)
        worker2 = Worker("player2", 2)
        self.assertEqual(worker2.player, "player2")
        self.assertEqual(worker2.number, 2)

    def test_worker_str(self):
        worker1 = Worker("player1", 1)
        self.assertEqual(str(worker1),'player11')

    def test_worker_bounds(self):
        """Test worker creation with out of bounds number."""
        with self.assertRaises(ValueError) as context:
            Worker("player1", 3)
        self.assertTrue("Worker number out of range!" in
                        str(context.exception))
        with self.assertRaises(ValueError) as context:
            Worker("player1", 0)
        self.assertTrue("Worker number out of range!" in
                        str(context.exception))

    def test_equality(self):
        """Test equality between workers"""
        self.assertEqual(Worker("player1", 1), Worker("player1", 1))

    def test_not_equality(self):
        """Test not equality between workers"""
        self.assertNotEqual(Worker("player2", 1), Worker("player1", 1))
        self.assertNotEqual(Worker("player2", 2), Worker("player2", 1))
        self.assertNotEqual(Worker("player2", 2), 4)

    def test_hash(self):
        """Test worker hashing using dictionary"""
        worker_dict = {Worker("player1", 1): 1,
                       Worker("player1", 2): 2,
                       Worker("player2", 1): 3,
                       Worker("player2", 2): 4,
                       Worker("player1", 1): 5}
        self.assertEqual(worker_dict[Worker("player1", 1)], 5)
        self.assertEqual(worker_dict[Worker("player1", 2)], 2)
        self.assertEqual(worker_dict[Worker("player2", 1)], 3)
        self.assertEqual(worker_dict[Worker("player2", 2)], 4)
