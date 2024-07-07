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
    def test_set_port_amigo(self, mock_grep):
        f = BaseFlasher()
        f.port = "amigo"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_port_amigo_tft(self, mock_grep):
        f = BaseFlasher()
        f.port = "amigo_tft"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_port_amigo_ips(self, mock_grep):
        f = BaseFlasher()
        f.port = "amigo_ips"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_port_m5stickv(self, mock_grep):
        f = BaseFlasher()
        f.port = "m5stickv"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_port_bit(self, mock_grep):
        f = BaseFlasher()
        f.port = "bit"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_ports_cube(self, mock_grep):
        f = BaseFlasher()
        f.port = "cube"
        mock_grep.assert_called_once_with("0403")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_port_dock(self, mock_grep):
        f = BaseFlasher()
        f.port = "dock"
        mock_grep.assert_called_once_with("7523")

    @patch(
        "src.utils.flasher.base_flasher.list_ports.grep", new_callable=MockListPortsGrep
    )
    def test_set_port_yahboom(self, mock_grep):
        f = BaseFlasher()
        f.port = "yahboom"
        mock_grep.assert_called_once_with("7523")

    def test_fail_set_port(self):
        with self.assertRaises(ValueError) as exc_info:
            f = BaseFlasher()
            f.port = "mock"

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
