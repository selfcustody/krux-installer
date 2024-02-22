from unittest import TestCase
from unittest.mock import patch, call
from src.utils.flasher import Flasher
from .shared_mocks import MockListPorts


class TestFlasher(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_flash(self, mock_process, mock_list_ports, mock_exists):
        f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
        f.flash()

        mock_exists.assert_has_calls(
            [
                call("mock/maixpy_test/kboot.kfpkg"),
                call("/mock/path"),
                call("/mock/path"),
            ]
        )

        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path",
            baudrate=1500000,
            board="dan",
            sram=False,
            file="mock/maixpy_test/kboot.kfpkg",
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
            )

        self.assertEqual(
            str(exc_info.exception),
            "Unavailable port: check if a valid device is connected",
        )
