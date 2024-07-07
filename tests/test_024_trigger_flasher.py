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
    @patch("src.utils.flasher.base_flasher.next")
    def test_detect_device_amigo(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.detect_device()

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_detect_device_amigo_tft(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo_tft/kboot.kfpkg"
        f.detect_device()

        mock_exists.assert_called_once_with("mock/maixpy_amigo_tft/kboot.kfpkg")
        mock_list_ports.grep.assert_has_calls([call("0403"), call("0403")])
        print(mock_next.mock_calls)
        assert len(mock_next.mock_calls) == 4

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_detect_device_amigo_ips(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo_ips/kboot.kfpkg"
        f.detect_device()

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo_ips/kboot.kfpkg")
        mock_list_ports.grep.assert_has_calls([call("0403"), call("0403")])
        assert len(mock_next.mock_calls) == 4

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_detect_device_dock(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_dock/kboot.kfpkg"
        f.detect_device()

        # patch assertios
        mock_exists.assert_called_once_with("mock/maixpy_dock/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("7523")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_detect_device_bit(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_bit/kboot.kfpkg"
        f.detect_device()

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_bit/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_detect_device_m5stickv(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_m5stickv/kboot.kfpkg"
        f.detect_device()

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_m5stickv/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_detect_device_yahboom(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_yahboom/kboot.kfpkg"
        f.detect_device()

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_yahboom/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("7523")
        mock_next.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_detect_device_cube(self, mock_next, mock_list_ports, mock_exists):
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_cube/kboot.kfpkg"
        f.detect_device()

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_cube/kboot.kfpkg")
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
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_flash_amigo(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        f.process_flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev=mock_next().device,
            baudrate=1500000,
            board="goE",
            file="mock/maixpy_amigo.kfpkg",
            callback=callback,
        )
        mock_list_ports.grep.assert_called_once_with("0403")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_flash_amigo_tft(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo_tft.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        f.process_flash(callback=callback)

        # patch_assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo_tft.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev=mock_next().device,
            baudrate=1500000,
            board="goE",
            file="mock/maixpy_amigo_tft.kfpkg",
            callback=callback,
        )
        mock_list_ports.grep.assert_has_calls([call("0403"), call("0403")])

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_flash_amigo_ips(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo_ips.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        f.process_flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo_ips.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev=mock_next().device,
            baudrate=1500000,
            board="goE",
            file="mock/maixpy_amigo_ips.kfpkg",
            callback=callback,
        )
        mock_list_ports.grep.assert_has_calls([call("0403"), call("0403")])

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_flash_m5stickv(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_m5stickv.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        f.process_flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_m5stickv.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev=mock_next().device,
            baudrate=1500000,
            board="goE",
            file="mock/maixpy_m5stickv.kfpkg",
            callback=callback,
        )
        mock_list_ports.grep.assert_called_once_with("0403")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_flash_dock(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_dock.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        f.process_flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_dock.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev=mock_next().device,
            baudrate=1500000,
            board="dan",
            file="mock/maixpy_dock.kfpkg",
            callback=callback,
        )
        mock_list_ports.grep.assert_called_once_with("7523")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_flash_bit(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_bit.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        f.process_flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_bit.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev=mock_next().device,
            baudrate=1500000,
            board="goE",
            file="mock/maixpy_bit.kfpkg",
            callback=callback,
        )
        mock_list_ports.grep.assert_called_once_with("0403")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_flash_yahboom(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_yahboom.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        f.process_flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_yahboom.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev=mock_next().device,
            baudrate=1500000,
            board="goE",
            file="mock/maixpy_yahboom.kfpkg",
            callback=callback,
        )
        mock_list_ports.grep.assert_called_once_with("7523")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_flash_cube(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_cube.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        f.process_flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_cube.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev=mock_next().device,
            baudrate=1500000,
            board="goE",
            file="mock/maixpy_cube.kfpkg",
            callback=callback,
        )
        mock_list_ports.grep.assert_called_once_with("0403")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_wipe_amigo(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        with patch.object(sys, "argv", []):
            f.process_wipe(callback=callback)
            mock_exists.assert_called_once_with("mock/maixpy_amigo.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", 1500000, "-p", mock_next().device, "-E"]
            )
            mock_list_ports.grep.assert_called_once_with("0403")
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_wipe_amigo_tft(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo_tft.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        with patch.object(sys, "argv", []):
            f.process_wipe(callback=callback)
            mock_exists.assert_called_once_with("mock/maixpy_amigo_tft.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", 1500000, "-p", mock_next().device, "-E"]
            )
            mock_list_ports.grep.assert_has_calls([call("0403"), call("0403")])
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_wipe_amigo_ips(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo_ips.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        with patch.object(sys, "argv", []):
            f.process_wipe(callback=callback)
            mock_exists.assert_called_once_with("mock/maixpy_amigo_ips.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", 1500000, "-p", mock_next().device, "-E"]
            )
            mock_list_ports.grep.assert_has_calls([call("0403"), call("0403")])
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_wipe_dock(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_dock.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        with patch.object(sys, "argv", []):
            f.process_wipe(callback=callback)
            mock_exists.assert_called_once_with("mock/maixpy_dock.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "dan", "-b", 1500000, "-p", mock_next().device, "-E"]
            )
            mock_list_ports.grep.assert_called_once_with("7523")
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_wipe_m5stickv(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_m5stickv.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        with patch.object(sys, "argv", []):
            f.process_wipe(callback=callback)
            mock_exists.assert_called_once_with("mock/maixpy_m5stickv.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", 1500000, "-p", mock_next().device, "-E"]
            )
            mock_list_ports.grep.assert_called_once_with("0403")
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_wipe_bit(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_bit.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        with patch.object(sys, "argv", []):
            f.process_wipe(callback=callback)
            mock_exists.assert_called_once_with("mock/maixpy_bit.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", 1500000, "-p", mock_next().device, "-E"]
            )
            mock_list_ports.grep.assert_called_once_with("0403")
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_wipe_yahboom(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_yahboom.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        with patch.object(sys, "argv", []):
            f.process_wipe(callback=callback)
            mock_exists.assert_called_once_with("mock/maixpy_yahboom.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", 1500000, "-p", mock_next().device, "-E"]
            )
            mock_list_ports.grep.assert_called_once_with("7523")
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    def test_process_wipe_cube(
        self, mock_next, mock_list_ports, mock_process, mock_exists
    ):
        callback = MagicMock()
        f = TriggerFlasher()
        f.firmware = "mock/maixpy_cube.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        with patch.object(sys, "argv", []):
            f.process_wipe(callback=callback)
            mock_exists.assert_called_once_with("mock/maixpy_cube.kfpkg")
            self.assertEqual(
                sys.argv, ["-B", "goE", "-b", 1500000, "-p", mock_next().device, "-E"]
            )
            mock_list_ports.grep.assert_called_once_with("0403")
            mock_process.assert_called_once()
            self.assertEqual(f.ktool.print_callback, callback)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_flash")
    def test_process_exception_flash(
        self, mock_process_flash, mock_list_ports, mock_exists
    ):
        callback = MagicMock()

        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        exc = Exception("Greeting fail: mock test")
        f.process_exception(exception=exc, process_type="flash", callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_process_flash.assert_called_once_with(callback=callback)
        mock_list_ports.grep.assert_called_once_with("0403")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.trigger_flasher.TriggerFlasher.process_wipe")
    def test_process_exception_wipe(
        self, mock_process_wipe, mock_list_ports, mock_exists
    ):
        callback = MagicMock()

        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        exc = Exception("Greeting fail: mock test")
        f.process_exception(exception=exc, process_type="wipe", callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_process_wipe.assert_called_once_with(callback=callback)
        mock_list_ports.grep.assert_called_once_with("0403")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    def test_fail_process_exception(self, mock_list_ports, mock_exists):
        callback = MagicMock()

        f = TriggerFlasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.detect_device()
        exc = Exception("Greeting success: mock fail")

        with self.assertRaises(RuntimeError) as exc_info:
            f.process_exception(exception=exc, process_type="flash", callback=callback)

        self.assertEqual(str(exc_info.exception), "Greeting success: mock fail")

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
