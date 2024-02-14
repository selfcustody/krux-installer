from unittest import TestCase
from unittest.mock import patch, call
from src.utils.flasher.base_flasher import BaseFlasher
from .shared_mocks import PropertyInstanceMock


class TestBaseFlasher(TestCase):

    @patch("os.path.exists", return_value=True)
    def test_init(self, mock_exists):
        f = BaseFlasher(firmware="mock/maixpy_test/kboot.kfpkg")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        self.assertEqual(f.firmware, "mock/maixpy_test/kboot.kfpkg")
        self.assertEqual(f.board, "goE")
        self.assertEqual(f.ktool.killProcess, False)
        self.assertEqual(f.ktool.loader, None)
        self.assertEqual(f.ktool.print_callback, None)

    @patch("os.path.exists", return_value=False)
    def test_init_fail(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            BaseFlasher(firmware="mock/maixpy_test/kboot.kfpkg")
            mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")

        self.assertEqual(
            str(exc_info.exception), "File do not exist: mock/maixpy_test/kboot.kfpkg"
        )

    @patch(
        "src.utils.flasher.base_flasher.BaseFlasher.board",
        new_callable=PropertyInstanceMock,
    )
    @patch("os.path.exists", return_value=True)
    def test_set_board(self, mock_exists, mock_board):
        f = BaseFlasher(firmware="mock/maixpy_test/kboot.kfpkg")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        f.board = "dan"
        mock_board.assert_has_calls([call(f, "goE"), call(f, "dan")])

    @patch("os.path.exists", return_value=True)
    def test_fail_set_board(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            f = BaseFlasher(firmware="mock/maixpy_test/kboot.kfpkg")
            mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
            f.board = "k210"
        self.assertEqual(str(exc_info.exception), "Invalid board: k210")
