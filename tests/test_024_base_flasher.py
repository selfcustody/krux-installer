from unittest import TestCase
from unittest.mock import patch
from src.utils.flasher.base_flasher import BaseFlasher
from .shared_mocks import PropertyInstanceMock, MockListPortsGrep


class TestBaseFlasher(TestCase):

    @patch("os.path.exists", return_value=True)
    def test_set_firmware(self, mock_exists):
        b = BaseFlasher()
        b.firmware = "mock/test/kboot.kfpkg"
        mock_exists.assert_called_once_with("mock/test/kboot.kfpkg")

    @patch("os.path.exists", return_value=False)
    def test_fail_set_firmware(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            b = BaseFlasher()
            b.firmware = "mock/test/kboot.kfpkg"
            mock_exists.assert_called_once_with("mock/test/kboot.kfpkg")

        self.assertEqual(
            str(exc_info.exception), "File do not exist: mock/test/kboot.kfpkg"
        )

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_ports_amigo(self, mock_grep):
        f = BaseFlasher()
        f.ports = "amigo"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_ports_amigo_tft(self, mock_grep):
        f = BaseFlasher()
        f.ports = "amigo_tft"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_ports_amigo_ips(self, mock_grep):
        f = BaseFlasher()
        f.ports = "amigo_ips"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_ports_m5stickv(self, mock_grep):
        f = BaseFlasher()
        f.ports = "m5stickv"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_ports_bit(self, mock_grep):
        f = BaseFlasher()
        f.ports = "bit"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_ports_cube(self, mock_grep):
        f = BaseFlasher()
        f.ports = "cube"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_ports_dock(self, mock_grep):
        f = BaseFlasher()
        f.ports = "dock"
        mock_grep.assert_called_once_with("7523")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_ports_yahboom(self, mock_grep):
        f = BaseFlasher()
        f.ports = "yahboom"
        mock_grep.assert_called_once_with("7523")

    def test_fail_set_ports(self):
        with self.assertRaises(ValueError) as exc_info:
            f = BaseFlasher()
            f.ports = "mock"

        self.assertEqual(str(exc_info.exception), "Device not implemented: mock")

    @patch(
        "src.utils.flasher.base_flasher.BaseFlasher.board",
        new_callable=PropertyInstanceMock,
    )
    def test_set_board_goe(self, mock_board):
        f = BaseFlasher()
        f.board = "goE"
        mock_board.assert_called_once_with(f, "goE")

    @patch(
        "src.utils.flasher.base_flasher.BaseFlasher.board",
        new_callable=PropertyInstanceMock,
    )
    def test_set_board_dan(self, mock_board):
        f = BaseFlasher()
        f.board = "dan"
        mock_board.assert_called_once_with(f, "dan")

    def test_fail_set_board(self):
        with self.assertRaises(ValueError) as exc_info:
            f = BaseFlasher()
            f.board = "mock"
        self.assertEqual(str(exc_info.exception), "Device not implemented: mock")
