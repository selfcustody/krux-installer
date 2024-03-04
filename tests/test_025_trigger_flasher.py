import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock
from serial.serialutil import SerialException
from src.utils.flasher.trigger_flasher import TriggerFlasher
from .shared_mocks import MockSerial


class TestTriggerFlasher(TestCase):

    def test_init(self):
        f = TriggerFlasher()
        self.assertEqual(f.ktool.killProcess, False)
        self.assertEqual(f.ktool.loader, None)
        self.assertEqual(f.ktool.print_callback, None)

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
