from unittest import TestCase
from unittest.mock import patch
from src.utils.flasher import Flasher, get_progress
from .shared_mocks import MockListPorts


class TestFlasher(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_flash(self, mock_process, mock_list_ports, mock_exists):
        f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
        f.flash()

        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path",
            baudrate=1500000,
            board="goE",
            sram=False,
            file="mock/maixpy_test/kboot.kfpkg",
            callback=get_progress,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    # pylint: disable=unused-argument
    def test_fail_flash(self, mock_process, mock_exists):

        mock_process.side_effect = RuntimeError

        with self.assertRaises(RuntimeError) as exc_info:
            f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
            f.flash()
            mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
            mock_process.assert_called_once_with(
                terminal=False,
                dev="/mock/path",
                baudrate=1500000,
                board="goE",
                sram=False,
                file="mock/maixpy_test/kboot.kfpkg",
                callback=get_progress,
            )

        self.assertEqual(str(exc_info.exception), "")
