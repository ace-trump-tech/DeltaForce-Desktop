# tests/test_downloader.py
import unittest
from core.downloader import Downloader

class TestDownloader(unittest.TestCase):
    def test_downloader_initialization(self):
        """Test that downloader loads config without errors."""
        try:
            d = Downloader()
            self.assertIsNotNone(d.config)
        except Exception as e:
            self.fail(f"Downloader init failed: {e}")
