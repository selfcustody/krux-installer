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
        mock_content_len.assert_called_once_with(downloader, 0)

    @patch(
        "src.utils.downloader.trigger_downloader.TriggerDownloader.filename",
        new_callable=PropertyInstanceMock,
    )
    def test_init_filename(self, mock_filename):
        downloader = TriggerDownloader(url=URL)
        mock_filename.assert_called_once_with(downloader, None)

    @patch(
        "src.utils.downloader.trigger_downloader.TriggerDownloader.downloaded_len",
        new_callable=PropertyInstanceMock,
    )
    def test_init_downloaded_len(self, mock_downloaded_len):
        downloader = TriggerDownloader(url=URL)
        mock_downloaded_len.assert_called_once_with(downloader, 0)

    @patch(
        "src.utils.downloader.trigger_downloader.TriggerDownloader.chunk_size",
        new_callable=PropertyInstanceMock,
    )
    def test_init_chunk_size(self, mock_chunk_size):
        downloader = TriggerDownloader(url=URL)
        mock_chunk_size.assert_called_once_with(downloader, 1024)
