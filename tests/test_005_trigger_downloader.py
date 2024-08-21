from unittest import TestCase
from unittest.mock import patch
from src.utils.downloader.trigger_downloader import TriggerDownloader
from .shared_mocks import PropertyInstanceMock

URL = "https://github.com/selfcustody/krux"


class TestTriggerDownloader(TestCase):

    @patch(
        "src.utils.downloader.trigger_downloader.TriggerDownloader.content_len",
        new_callable=PropertyInstanceMock,
    )
    def test_init_content_len(self, mock_content_len):
        downloader = TriggerDownloader(url=URL)
        downloader.content_len = 0
        mock_content_len.assert_called_once_with(downloader, 0)

    @patch(
        "src.utils.downloader.trigger_downloader.TriggerDownloader.filename",
        new_callable=PropertyInstanceMock,
    )
    def test_init_filename(self, mock_filename):
        downloader = TriggerDownloader(url=URL)
        downloader.filename = "mockfile"
        mock_filename.assert_called_once_with(downloader, "mockfile")

    @patch(
        "src.utils.downloader.trigger_downloader.TriggerDownloader.downloaded_len",
        new_callable=PropertyInstanceMock,
    )
    def test_init_downloaded_len(self, mock_downloaded_len):
        downloader = TriggerDownloader(url=URL)
        downloader.downloaded_len = 0
        mock_downloaded_len.assert_called_once_with(downloader, 0)

    def test_set_chunk_size(self):
        downloader = TriggerDownloader(url=URL)
        downloader.chunk_size = 1024
        self.assertEqual(downloader.chunk_size, 1024)

    def test_fail_set_chunk_size(self):
        downloader = TriggerDownloader(url=URL)
        with self.assertRaises(ValueError) as exc_info:
            downloader.chunk_size = 1025

        self.assertEqual(str(exc_info.exception), "1025 isnt a power of 2")
