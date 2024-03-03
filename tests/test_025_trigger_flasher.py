from unittest import TestCase
from unittest.mock import patch, MagicMock
from serial.serialutil import SerialException
from src.utils.flasher.trigger_flasher import TriggerFlasher
from .shared_mocks import MockListPorts, MockSerial


class TestTriggerFlasher(TestCase):

    def test_init(self):
        f = TriggerFlasher()
        self.assertEqual(f.ktool.killProcess, False)
        self.assertEqual(f.ktool.loader, None)
        self.assertEqual(f.ktool.print_callback, None)

    @patch(
        "src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts
    )
    def test_detect_port_amigo(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="amigo")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")

    @patch(
        "src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts
    )
    def test_detect_port_amigo_tft(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="amigo")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")

    @patch(
        "src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts
    )
    def test_detect_port_amigo_ips(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="amigo")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")

    @patch(
        "src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts
    )
    def test_detect_port_m5stickv(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="m5stickv")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")

    @patch(
        "src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts
    )
    def test_detect_port_bit(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="m5stickv")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")

    @patch(
        "src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts
    )
    def test_detect_port_dock(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="dock")
        mock_grep.assert_called_once_with("7523")
        self.assertEqual(f.board, "dan")

    @patch(
        "src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts
    )
    def test_detect_port_yahboom(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="yahboom")
        mock_grep.assert_called_once_with("7523")
        self.assertEqual(f.board, "goE")

    @patch("src.utils.flasher.trigger_flasher.Serial", new_callable=MockSerial)
    def test_is_port_working(self, mock_serial):
        f = TriggerFlasher()
        result = f.is_port_working("/mock/path0")
        mock_serial.assert_called_once_with("/mock/path0")
        self.assertEqual(result, True)

    @patch("src.utils.flasher.trigger_flasher.Serial", side_effect=SerialException)
    def test_not_is_port_working(self, mock_serial):
        f = TriggerFlasher()
        result = f.is_port_working("/mock/path0")
        mock_serial.assert_called_once_with("/mock/path0")
        self.assertEqual(result, False)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_flash_no_callback(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "goE"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0")
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="goE",
            file="mock/firmware.kfpkg",
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_flash_callback(self, mock_process, mock_exists):
        mock_callback = MagicMock()
        f = TriggerFlasher()
        f.board = "goE"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0", callback=mock_callback)
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="goE",
            file="mock/firmware.kfpkg",
            callback=mock_callback,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_no_callback(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "goE"
        f.firmware = "mock/firmware.kfpkg"
        f.process_wipe("/mock/path0")
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once()
