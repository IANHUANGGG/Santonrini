import unittest
import time
from santorini.aux.timeout import Timeout

class TestTimeout(unittest.TestCase):

    def test_timeout_works(self):
        with self.assertRaises(Exception) as context:
            with Timeout(1):
                time.sleep(2)

        self.assertTrue('Timed out' in str(context.exception))
