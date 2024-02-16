from unittest import TestCase
from unittest.mock import patch
from src.utils.flasher import Flasher


class TestFlasher(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_flash(self, mock_process, mock_exists):
        f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")

        # pylint: disable=unused-argument
        def get_progress(file_type_str, iteration, total, suffix):
            pass

        f.flash(callback=get_progress)

        mock_process.assert_any_call(
            terminal=False,
            dev="DEFAULT",
            baudrate=1500000,
            board="goE",
            sram=False,
            file="mock/maixpy_test/kboot.kfpkg",
            callback=get_progress,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    def test_fail_flash(self, mock_process, mock_exists):

        mock_process.side_effect = RuntimeError

        with self.assertRaises(RuntimeError) as exc_info:
            f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
            mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
            f.flash()

        self.assertEqual(str(exc_info.exception), "None")
