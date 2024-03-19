from unittest import TestCase
from unittest.mock import patch
from src.utils.downloader import ZipDownloader


class TestZipDownloader(TestCase):

    @patch("tempfile.gettempdir")
    def test_init_url(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        z = ZipDownloader(version="v0.0.1")
        self.assertEqual(
            z.url,
            "https://github.com/selfcustody/krux/releases/download/v0.0.1/krux-v0.0.1.zip",
        )

    @patch("tempfile.gettempdir")
    def test_init_destdir(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        z = ZipDownloader(version="v0.0.1", destdir=mock_gettempdir())
        self.assertEqual(z.destdir, "/tmp/dir")

    @patch("tempfile.gettempdir")
    def test_init_write_mode(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        z = ZipDownloader(version="v0.0.1", destdir=mock_gettempdir())
        self.assertEqual(z.write_mode, "wb")
