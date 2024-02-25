from unittest import TestCase
from unittest.mock import patch, call
from src.utils.flasher.base_flasher import BaseFlasher
from .shared_mocks import PropertyInstanceMock, MockSerial


class TestBaseFlasher(TestCase):

    def test_init(self):
        f = BaseFlasher()
        self.assertEqual(f.ktool.killProcess, False)
        self.assertEqual(f.ktool.loader, None)
        self.assertEqual(f.ktool.print_callback, None)

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

    @patch("sys.platform", "linux")
    @patch("os.path.exists", return_value=True)
    def test_set_port_linux(self, mock_exists):
        f = BaseFlasher()
        f.port = "/dev/ttymock"
        mock_exists.assert_called_once_with("/dev/ttymock")

    @patch("sys.platform", "linux")
    @patch("os.path.exists", return_value=False)
    def test_fail_set_port_linux(self, mock_exists):
        with self.assertRaises(OSError) as exc_info:
            f = BaseFlasher()
            f.port = "/dev/ttymock"
            mock_exists.assert_called_once_with("/dev/ttymock")
        self.assertEqual(str(exc_info.exception), "Port do not exist: /dev/ttymock")

    @patch("sys.platform", "darwin")
    @patch("os.path.exists", return_value=True)
    def test_set_port_mac(self, mock_exists):
        f = BaseFlasher()
        f.port = "/dev/tty.mock"
        mock_exists.assert_called_once_with("/dev/tty.mock")

    @patch("sys.platform", "darwin")
    @patch("os.path.exists", return_value=False)
    def test_fail_set_port_darwin(self, mock_exists):
        with self.assertRaises(OSError) as exc_info:
            f = BaseFlasher()
            f.port = "/dev/tty.mock"
            mock_exists.assert_called_once_with("/dev/tty.mock")
        self.assertEqual(str(exc_info.exception), "Port do not exist: /dev/tty.mock")

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.base_flasher.Serial")
    def test_set_port_win(self, mock_serial):
        mock_serial.side_effect = MockSerial
        f = BaseFlasher()
        f.port = "COM0"
        mock_serial.assert_called_once_with("COM0")

    @patch("sys.platform", "win32")
    def test_fail_os_set_port_win(self):
        msgs = [
            "[Errno 2] could not open port COM0: [Errno 2] No such file or directory: 'COM0'",
            "could not open port 'COM0':"
            + " FileNotFoundError(2, 'The system cannot find the file specified.', None, 2)",
        ]
        with self.assertRaises(OSError) as exc_info:
            f = BaseFlasher()
            f.port = "COM0"

        self.assertIn(str(exc_info.exception), msgs)

    @patch("sys.platform", "oracle")
    def test_fail_set_port_oracle(self):
        with self.assertRaises(EnvironmentError) as exc_info:
            f = BaseFlasher()
            f.port = "COM0"
        self.assertEqual(str(exc_info.exception), "Unsupported platform: oracle")

    @patch(
        "src.utils.flasher.base_flasher.BaseFlasher.board",
        new_callable=PropertyInstanceMock,
    )
    def test_set_board(self, mock_board):
        f = BaseFlasher()
        f.board = "goE"
        f.board = "dan"
        mock_board.assert_has_calls([call(f, "goE"), call(f, "dan")])

    def test_fail_set_board(self):
        with self.assertRaises(ValueError) as exc_info:
            f = BaseFlasher()
            f.board = "k210"
        self.assertEqual(str(exc_info.exception), "Invalid board: k210")
