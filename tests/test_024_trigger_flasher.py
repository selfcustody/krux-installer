import sys
from unittest import TestCase
from unittest.mock import patch, call, MagicMock
from serial.serialutil import SerialException
from src.utils.flasher.trigger_flasher import TriggerFlasher
from .shared_mocks import MockSerial, MockListPortsGrep


class TestTriggerFlasher(TestCase):

    def test_init(self):
        f = TriggerFlasher()
        self.assertEqual(f.ktool.killProcess, False)
        self.assertEqual(f.ktool.loader, None)
        self.assertEqual(f.ktool.print_callback, None)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.next")
    def test_get_port_amigo(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_test/kboot.kfpkg"
        f.get_port(device="amigo")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.next")
    def test_get_port_amigo_tft(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_test/kboot.kfpkg"
        f.get_port(device="amigo_tft")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.next")
    def test_get_port_amigo_ips(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_test/kboot.kfpkg"
        f.get_port(device="amigo_ips")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.next")
    def test_get_port_dock(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_test/kboot.kfpkg"
        f.get_port(device="dock")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("7523")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.next")
    def test_get_port_bit(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_test/kboot.kfpkg"
        f.get_port(device="bit")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.next")
    def test_get_port_m5stickv(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_test/kboot.kfpkg"
        f.get_port(device="m5stickv")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.next")
    def test_get_port_yahboom(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_test/kboot.kfpkg"
        f.get_port(device="yahboom")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("7523")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.next")
    def test_get_port_cube(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_test/kboot.kfpkg"
        f.get_port(device="cube")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()

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
    def test_process_flash_no_callback_amigo(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "amigo"
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
    def test_process_flash_callback_amigo(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "amigo"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0", callback=callback)
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="goE",
            file="mock/firmware.kfpkg",
            callback=callback,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_flash_no_callback_amigo_tft(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "amigo_tft"
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
    def test_process_flash_callback_amigo_tft(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "amigo_tft"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0", callback=callback)
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="goE",
            file="mock/firmware.kfpkg",
            callback=callback,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_flash_no_callback_amigo_ips(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "amigo_ips"
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
    def test_process_flash_callback_amigo_ips(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "amigo_ips"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0", callback=callback)
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="goE",
            file="mock/firmware.kfpkg",
            callback=callback,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_flash_no_callback_m5stickv(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "m5stickv"
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
    def test_process_flash_callback_m5stickv(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "m5stickv"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0", callback=callback)
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="goE",
            file="mock/firmware.kfpkg",
            callback=callback,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_flash_no_callback_dock(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "dock"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0")
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="dan",
            file="mock/firmware.kfpkg",
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_flash_callback_dock(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "dock"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0", callback=callback)
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="dan",
            file="mock/firmware.kfpkg",
            callback=callback,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_flash_no_callback_bit(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "bit"
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
    def test_process_flash_callback_bit(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "bit"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0", callback=callback)
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="goE",
            file="mock/firmware.kfpkg",
            callback=callback,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_flash_no_callback_cube(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "cube"
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
    def test_process_flash_callback_cube(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "cube"
        f.firmware = "mock/firmware.kfpkg"
        f.process_flash("/mock/path0", callback=callback)
        mock_exists.assert_called_once_with("mock/firmware.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path0",
            baudrate=1500000,
            board="goE",
            file="mock/firmware.kfpkg",
            callback=callback,
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_no_callback_amigo(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "amigo"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0")
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_callback_amigo(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "amigo"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0", callback=callback)
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_no_callback_amigo_tft(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "amigo_tft"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0")
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_callback_amigo_tft(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "amigo_tft"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0", callback=callback)
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_no_callback_amigo_ips(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "amigo_ips"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0")
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_callback_amigo_ips(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "amigo_ips"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0", callback=callback)
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_no_callback_dock(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "dock"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0")
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "dan", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_callback_dock(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "dock"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0", callback=callback)
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "dan", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_no_callback_m5stickv(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "m5stickv"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0")
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_callback_m5stickv(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "m5stickv"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0", callback=callback)
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_no_callback_bit(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "bit"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0")
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_callback_bit(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "bit"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0", callback=callback)
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_no_callback_cube(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "cube"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0")
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_callback_cube(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "cube"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0", callback=callback)
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_no_callback_yahboom(self, mock_process, mock_exists):
        f = TriggerFlasher()
        f.board = "yahboom"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0")
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    def test_process_wipe_callback_yahboom(self, mock_process, mock_exists):
        callback = MagicMock()
        f = TriggerFlasher()
        f.board = "yahboom"
        f.firmware = "mock/firmware.kfpkg"
        with patch.object(sys, "argv", []):
            f.process_wipe("/mock/path0", callback=callback)
            mock_exists.assert_called_once_with("mock/firmware.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", "1500000", "-p", "/mock/path0", "-E"]
            )
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("sys.platform", "linux")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_flash")
    def test_process_exception_no_callback_flash_linux(
        self, mock_process_flash, mock_re
    ):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0", exc_info=exc, process=f.process_flash
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_flash.assert_called_once_with(
                port="/mock/path1", callback=None
            )

    @patch("sys.platform", "darwin")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_flash")
    def test_process_exception_no_callback_flash_darwin(
        self, mock_process_flash, mock_re
    ):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0", exc_info=exc, process=f.process_flash
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_flash.assert_called_once_with(
                port="/mock/path1", callback=None
            )

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_flash")
    def test_process_exception_no_callback_flash_win32(
        self, mock_process_flash, mock_re
    ):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(oldport="MOCK0", exc_info=exc, process=f.process_flash)
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_flash.assert_called_once_with(port="MOCK1", callback=None)

    @patch("sys.platform", "linux")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_flash")
    def test_process_exception_callback_flash_linux(self, mock_process_flash, mock_re):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            callback = MagicMock()
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0",
                exc_info=exc,
                process=f.process_flash,
                callback=callback,
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_flash.assert_called_once_with(
                port="/mock/path1", callback=callback
            )

    @patch("sys.platform", "darwin")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_flash")
    def test_process_exception_callback_flash_darwin(self, mock_process_flash, mock_re):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            callback = MagicMock()
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0",
                exc_info=exc,
                process=f.process_flash,
                callback=callback,
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_flash.assert_called_once_with(
                port="/mock/path1", callback=callback
            )

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_flash")
    def test_process_exception_callback_flash_win32(self, mock_process_flash, mock_re):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            callback = MagicMock()
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="MOCK0",
                exc_info=exc,
                process=f.process_flash,
                callback=callback,
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_flash.assert_called_once_with(port="MOCK1", callback=callback)

    @patch("sys.platform", "linux")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_wipe")
    def test_process_exception_no_callback_wipe_linux(self, mock_process_wipe, mock_re):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0", exc_info=exc, process=f.process_wipe
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_wipe.assert_called_once_with(port="/mock/path1", callback=None)

    @patch("sys.platform", "darwin")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_wipe")
    def test_process_exception_no_callback_wipe_darwin(
        self, mock_process_wipe, mock_re
    ):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0", exc_info=exc, process=f.process_wipe
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_wipe.assert_called_once_with(port="/mock/path1", callback=None)

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_wipe")
    def test_process_exception_no_callback_wipe_win32(self, mock_process_wipe, mock_re):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(oldport="MOCK0", exc_info=exc, process=f.process_wipe)
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_wipe.assert_called_once_with(port="MOCK1", callback=None)

    @patch("sys.platform", "linux")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_wipe")
    def test_process_exception_callback_wipe_linux(self, mock_process_wipe, mock_re):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            callback = MagicMock()
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0",
                exc_info=exc,
                process=f.process_wipe,
                callback=callback,
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_wipe.assert_called_once_with(
                port="/mock/path1", callback=callback
            )

    @patch("sys.platform", "darwin")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_wipe")
    def test_process_exception_callback_wipe_darwin(self, mock_process_wipe, mock_re):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            callback = MagicMock()
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0",
                exc_info=exc,
                process=f.process_wipe,
                callback=callback,
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_wipe.assert_called_once_with(
                port="/mock/path1", callback=callback
            )

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.trigger_flasher.re")
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_wipe")
    def test_process_exception_callback_wipe_win32(self, mock_process_wipe, mock_re):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            callback = MagicMock()
            exc = Exception("Greeting fail: mock test")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="MOCK0",
                exc_info=exc,
                process=f.process_wipe,
                callback=callback,
            )
            mock_re.findall.assert_called_once_with(
                r"Greeting fail", "Greeting fail: mock test"
            )
            mock_next.assert_has_calls([call(f.ports), call(f.ports)])
            mock_process_wipe.assert_called_once_with(port="MOCK1", callback=callback)

    @patch("sys.platform", "linux")
    @patch("builtins.print")
    def test_process_exception_print_no_callback_linux(self, mock_print):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            exc = Exception("Unknown mocked error")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0",
                exc_info=exc,
            )
            mock_next.assert_has_calls([call(f.ports)])
            mock_print.assert_called_once_with(
                "\033[31;1m[ERROR]\033[0m Unknown mocked error"
            )

    @patch("sys.platform", "linux")
    def test_process_exception_print_callback_linux(self):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            callback = MagicMock()
            exc = Exception("Unknown mocked error")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(oldport="/mock/path0", exc_info=exc, callback=callback)
            mock_next.assert_has_calls([call(f.ports)])
            callback.assert_called_once_with("Unknown mocked error")

    @patch("sys.platform", "darwin")
    @patch("builtins.print")
    def test_process_exception_print_no_callback_darwin(self, mock_print):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            exc = Exception("Unknown mocked error")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="/mock/path0",
                exc_info=exc,
            )
            mock_next.assert_has_calls([call(f.ports)])
            mock_print.assert_called_once_with(
                "\033[31;1m[ERROR]\033[0m Unknown mocked error"
            )

    @patch("sys.platform", "darwin")
    def test_process_exception_print_callback_darwin(self):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            callback = MagicMock()
            exc = Exception("Unknown mocked error")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(oldport="/mock/path0", exc_info=exc, callback=callback)
            mock_next.assert_has_calls([call(f.ports)])
            callback.assert_called_once_with("Unknown mocked error")

    @patch("sys.platform", "win32")
    @patch("builtins.print")
    def test_process_exception_print_no_callback_win32(self, mock_print):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            exc = Exception("Unknown mocked error")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(
                oldport="MOCK0",
                exc_info=exc,
            )
            mock_next.assert_has_calls([call(f.ports)])
            mock_print.assert_called_once_with(
                "\033[31;1m[ERROR]\033[0m Unknown mocked error"
            )

    @patch("sys.platform", "win32")
    def test_process_exception_print_callback_win32(self):
        with patch(
            "src.utils.flasher.trigger_flasher.next",
            return_value=MockListPortsGrep().devices[1],
        ) as mock_next:
            callback = MagicMock()
            exc = Exception("Unknown mocked error")
            f = TriggerFlasher()
            f.get_port(device="amigo")
            f.process_exception(oldport="MOCK0", exc_info=exc, callback=callback)
            mock_next.assert_has_calls([call(f.ports)])
            callback.assert_called_once_with("Unknown mocked error")
