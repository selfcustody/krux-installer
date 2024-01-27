from unittest import TestCase
from unittest.mock import patch
from src.utils.downloader.trigger_downloader import TriggerDownloader


class TestTriggerDownloader(TestCase):
    def test_init(self):
        downloader = TriggerDownloader()
        self.assertTrue(downloader.buffer is not None)

    @patch("src.utils.downloader.trigger_downloader.BytesIO")
    def test_cannot_set(self, mock_io):
        downloader = TriggerDownloader()
        with self.assertRaises(AttributeError) as exc_info:
            downloader.buffer = mock_io

        self.assertEqual(str(exc_info.exception), "You're forbidden to set buffer")
