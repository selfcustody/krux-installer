from unittest import TestCase
from unittest.mock import patch
from src.utils.flasher import Flasher
from .shared_mocks import MockListPortsGrep


class TestFlasher(TestCase):

    @patch("sys.platform", "linux")
    @patch("os.path.exists", return_value=True)
    @patch(
        "src.utils.flasher.trigger_flasher.list_ports.grep",
        new_callable=MockListPortsGrep,
    )
    def test_flash_linux_amigo_ttyusb0(self, mock_grep, mock_exists):
        f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
        f.flash(device="amigo")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_grep.assert_called_once_with("0403")
        # mock_serial.assert_called_once_with("/mock/path0")
        # mock_process.assert_called_once_with(
        #    terminal=False,
        #    dev="/mock/path0",
        #    baudrate=1500000,
        #    board="goE",
        #    sram=False,
        #    file="mock/maixpy_test/kboot.kfpkg",
        # )
