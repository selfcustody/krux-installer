from unittest import TestCase
from unittest.mock import patch, MagicMock
from src.utils.flasher import Flasher
from .shared_mocks import MockListPortsGrep


class TestFlasher(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.flasher.flasher.Flasher.process_flash")
    def test_flash_success(
        self,
        mock_process_flash,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_called_once_with(mock_next().device)
        mock_process_flash.assert_called_once_with(callback=callback)

    @patch("os.path.exists", return_value=False)
    def test_fail_flash_firmware_not_exist(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            f = Flasher()
            f.firmware = "mock/maixpy_amigo/kboot.kfpkg"

        self.assertEqual(
            str(exc_info.exception), "File do not exist: mock/maixpy_amigo/kboot.kfpkg"
        )
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")

    @patch("os.path.exists", return_value=True)
    def test_fail_flash_wrong_baudrate(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            f = Flasher()
            f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
            f.baudrate = 1234567

        self.assertEqual(str(exc_info.exception), "Invalid baudrate: 1234567")
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=False)
    def test_fail_port_not_working(
        self, mock_is_port_working, mock_next, mock_list_ports, mock_exists
    ):
        callback = MagicMock()
        with self.assertRaises(RuntimeError) as exc_info:
            f = Flasher()
            f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
            f.baudrate = 1500000
            f.flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_called_once_with(mock_next().device)

        # default assertions
        self.assertEqual(
            str(exc_info.exception), f"Port not working: {mock_next().device}"
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.flasher.Flasher.process_exception")
    def test_flash_greeting_fail(
        self,
        mock_process_exception,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        mock_exception = Exception("Greeting fail: mock test")
        mock_process.side_effect = [mock_exception, True]

        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_called_once_with(mock_next().device)
        mock_process_exception.assert_called_once_with(
            exception=mock_exception, process_type="flash", callback=callback
        )
        mock_process.assert_called_once_with(
            terminal=False,
            dev=mock_next().device,
            baudrate=1500000,
            board="goE",
            file="mock/maixpy_amigo/kboot.kfpkg",
            callback=callback,
        )
