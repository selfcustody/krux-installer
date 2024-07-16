from unittest import TestCase
from unittest.mock import patch
from src.utils.downloader.base_downloader import BaseDownloader
from .shared_mocks import PropertyInstanceMock


class TestBaseDownloader(TestCase):

    @patch(
        "src.utils.downloader.base_downloader.BaseDownloader.buffer",
        new_callable=PropertyInstanceMock,
    )
    @patch(
        "src.utils.downloader.base_downloader.BaseDownloader.url",
        new_callable=PropertyInstanceMock,
    )
    def test_init_selfcustody(self, mock_url, mock_buffer):
        url = "https://github.com/selfcustody/krux"
        downloader = BaseDownloader(url=url)

        self.assertTrue(downloader.buffer is not None)
        mock_buffer.assert_called_once_with(downloader)
        mock_url.assert_called_once_with(downloader, url)

    @patch(
        "src.utils.downloader.base_downloader.BaseDownloader.buffer",
        new_callable=PropertyInstanceMock,
    )
    @patch(
        "src.utils.downloader.base_downloader.BaseDownloader.url",
        new_callable=PropertyInstanceMock,
    )
    def test_init_selfcustody_raw(self, mock_url, mock_buffer):
        url = "https://raw.githubusercontent.com/selfcustody/krux"
        downloader = BaseDownloader(url=url)

        self.assertTrue(downloader.buffer is not None)
        mock_buffer.assert_called_once_with(downloader)
        mock_url.assert_called_once_with(downloader, url)

    @patch(
        "src.utils.downloader.base_downloader.BaseDownloader.buffer",
        new_callable=PropertyInstanceMock,
    )
    @patch(
        "src.utils.downloader.base_downloader.BaseDownloader.url",
        new_callable=PropertyInstanceMock,
    )
    def test_init_odudex(self, mock_url, mock_buffer):
        url = "https://github.com/odudex/krux_binaries"
        downloader = BaseDownloader(url=url)

        self.assertTrue(downloader.buffer is not None)
        mock_buffer.assert_called_once_with(downloader)
        mock_url.assert_called_once_with(downloader, url)

    @patch(
        "src.utils.downloader.base_downloader.BaseDownloader.buffer",
        new_callable=PropertyInstanceMock,
    )
    @patch(
        "src.utils.downloader.base_downloader.BaseDownloader.url",
        new_callable=PropertyInstanceMock,
    )
    def test_init_odudex_raw(self, mock_url, mock_buffer):
        url = "https://raw.githubusercontent.com/odudex/krux_binaries"
        downloader = BaseDownloader(url=url)

        self.assertTrue(downloader.buffer is not None)
        mock_buffer.assert_called_once_with(downloader)
        mock_url.assert_called_once_with(downloader, url)

    def test_fail_init(self):
        url = "https://gitlab.com/selfcustody/krux"

        with self.assertRaises(ValueError) as exc_info:
            BaseDownloader(url=url)

        self.assertEqual(
            str(exc_info.exception), "Invalid url: https://gitlab.com/selfcustody/krux"
        )
