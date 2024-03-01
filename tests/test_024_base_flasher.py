from unittest import TestCase
from unittest.mock import patch, call
from src.utils.flasher.base_flasher import BaseFlasher
from .shared_mocks import PropertyInstanceMock


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
        "src.utils.flasher.base_flasher.BaseFlasher.ports",
        new_callable=PropertyInstanceMock,
    )
    def test_set_ports(self, mock_ports):
        f = BaseFlasher()
        generator = iter(["/dev/ttymock0"])
        f.ports = generator
        mock_ports.assert_called_once_with(f, generator)

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
