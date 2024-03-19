from unittest import TestCase
from unittest.mock import patch, call
from src.utils.downloader import BetaDownloader
from .shared_mocks import PropertyInstanceMock


BASE_URL = "https://raw.githubusercontent.com/odudex/krux_binaries/main"


class TestBetaDownloader(TestCase):

    @patch(
        "src.utils.downloader.BetaDownloader.device", new_callable=PropertyInstanceMock
    )
    @patch(
        "src.utils.downloader.BetaDownloader.binary_type",
        new_callable=PropertyInstanceMock,
    )
    @patch("tempfile.gettempdir")
    def test_calls_init(self, mock_gettempdir, mock_binary_type, mock_device):
        mock_gettempdir.return_value = "/tmp/dir"

        devices = ("amigo_tft", "amigo_ips", "bit", "dock", "yahboom")
        binary_types = ("firmware.bin", "kboot.kfpkg")

        for device in devices:
            for _bin in binary_types:
                b = BetaDownloader(
                    device=device, binary_type=_bin, destdir=mock_gettempdir()
                )
                mock_device.assert_has_calls([call(b, device)])
                mock_binary_type.assert_has_calls([call(b, _bin)])

    @patch("tempfile.gettempdir")
    def test_init_url(self, mock_gettempdir):
        devices = ("amigo_tft", "amigo_ips", "bit", "dock", "yahboom")
        binary_types = ("firmware.bin", "kboot.kfpkg")

        mock_gettempdir.return_value = "/tmp/dir"
        for device in devices:
            for _bin in binary_types:
                mock_url = f"{BASE_URL}/maixpy_{device}/{_bin}"
                b = BetaDownloader(
                    device=device, binary_type=_bin, destdir=mock_gettempdir()
                )
                self.assertEqual(b.url, mock_url)

    @patch("tempfile.gettempdir")
    def test_fail_init_device(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        with self.assertRaises(ValueError) as exc_info:
            BetaDownloader(
                device="lilygo", binary_type="firmware", destdir=mock_gettempdir()
            )

        self.assertEqual(str(exc_info.exception), "Invalid device lilygo")

    @patch("tempfile.gettempdir")
    def test_fail_binary_type(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        with self.assertRaises(ValueError) as exc_info:
            BetaDownloader(
                device="amigo_tft", binary_type="esp32", destdir=mock_gettempdir()
            )

        self.assertEqual(str(exc_info.exception), "Invalid binary_type esp32")

    @patch("tempfile.gettempdir")
    def test_init_destdir(self, mock_gettempdir):
        devices = ("amigo_tft", "amigo_ips", "bit", "dock", "yahboom")
        binary_types = ("firmware.bin", "kboot.kfpkg")

        mock_gettempdir.return_value = "/tmp/dir"
        for device in devices:
            for _bin in binary_types:
                b = BetaDownloader(
                    device=device, binary_type=_bin, destdir=mock_gettempdir()
                )
                self.assertEqual(b.destdir, "/tmp/dir")

    @patch("tempfile.gettempdir")
    def test_init_write_mode(self, mock_gettempdir):
        devices = ("amigo_tft", "amigo_ips", "bit", "dock", "yahboom")
        binary_types = ("firmware.bin", "kboot.kfpkg")

        mock_gettempdir.return_value = "/tmp/dir"
        for device in devices:
            for _bin in binary_types:
                b = BetaDownloader(
                    device=device, binary_type=_bin, destdir=mock_gettempdir()
                )
                self.assertEqual(b.write_mode, "wb")
