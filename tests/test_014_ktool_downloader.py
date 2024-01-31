from unittest import TestCase
from unittest.mock import patch
from src.utils.downloader import KtoolDownloader


BASE_URL = "https://raw.githubusercontent.com/odudex/krux_binaries/main"


class TestBetaDownloader(TestCase):

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Linux")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_linux(self, mock_gettempdir, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-linux")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Windows")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_windows(self, mock_gettempdir, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-win32.exe")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="10.6.8")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_snow_leopard(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac-10")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="10.8.2")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_mountain_lion(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac-10")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="10.9.5")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mavericks(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac-10")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="10.10.1")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_yosemite(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac-10")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="10.11.6")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_el_captain(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac-10")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="10.12.6")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_sierra(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac-10")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="10.13.6")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_high_sierra(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac-10")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="10.14.6")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_mojave(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac-10")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="10.15.7")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_catalina(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac-10")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="11.7.10")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_big_sur(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="12.7.3")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_monterey(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="13.6.4")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_ventura(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="14.3")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_init_mac_sonoma(self, mock_gettempdir, mock_mac, mock_system):
        k = KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(k.url, f"{BASE_URL}/ktool-mac")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="Darwin")
    @patch("src.utils.downloader.ktool_downloader.mac_ver", return_value="9.1.2")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_fail_init_mac(self, mock_gettempdir, mock_mac, mock_system):
        with self.assertRaises(NotImplementedError) as exc_info:
            KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(str(exc_info.exception), "Not supported mac version: 9.1.2")

    @patch("src.utils.downloader.ktool_downloader.system", return_value="SunOS")
    @patch("tempfile.gettempdir", return_value="/tmp/dir")
    # pylint: disable=unused-argument
    def test_fail_init_sunos(self, mock_gettempdir, mock_system):
        with self.assertRaises(NotImplementedError) as exc_info:
            KtoolDownloader(destdir=mock_gettempdir())
        self.assertEqual(str(exc_info.exception), "Not supported platform: SunOS")
