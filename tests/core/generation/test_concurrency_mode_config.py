import unittest

from config.settings import CONCURRENCY_MODE


class TestConcurrencyModeConfig(unittest.TestCase):
    def test_concurrency_mode_fixed_send_api(self):
        self.assertEqual(CONCURRENCY_MODE, "send_api")


if __name__ == "__main__":
    unittest.main()
