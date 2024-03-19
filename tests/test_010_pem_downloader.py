from unittest import TestCase
from unittest.mock import patch
from src.utils.downloader import PemDownloader


URL = "https://raw.githubusercontent.com/selfcustody/krux/main/selfcustody.pem"


class TestPemDownloader(TestCase):

    @patch("tempfile.gettempdir")
    def test_init_url(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        z = PemDownloader()
        self.assertEqual(z.url, URL)

    @patch("tempfile.gettempdir")
    def test_init_destdir(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        z = PemDownloader(destdir=mock_gettempdir())
        self.assertEqual(z.destdir, "/tmp/dir")

    @patch("tempfile.gettempdir")
    def test_init_write_mode(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        z = PemDownloader(destdir=mock_gettempdir())
        self.assertEqual(z.write_mode, "w")
