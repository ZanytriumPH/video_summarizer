import unittest

from config.settings import resolve_concurrency_mode


class TestConcurrencyModeConfig(unittest.TestCase):
    def test_resolve_mode_accepts_threadpool(self):
        self.assertEqual(resolve_concurrency_mode("threadpool"), "threadpool")

    def test_resolve_mode_accepts_send_api(self):
        self.assertEqual(resolve_concurrency_mode("send_api"), "send_api")

    def test_resolve_mode_fallbacks_on_invalid_value(self):
        self.assertEqual(resolve_concurrency_mode("invalid_mode"), "threadpool")


if __name__ == "__main__":
    unittest.main()
