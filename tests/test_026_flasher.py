from unittest import TestCase
from unittest.mock import patch, MagicMock
from src.utils.flasher import Flasher
from .shared_mocks import MockListPortsGrep


class TestFlasher(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch(
        "src.utils.flasher.flasher.Flasher.get_port",
        return_value=MagicMock(device="/mock/path0"),
    )
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.flasher.flasher.Flasher.process_flash")
    def test_flash_amigo_no_callback(
        self, mock_process_flash, mock_is_port_working, mock_get_port, mock_exists
    ):
        f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
        f.flash(device="amigo")
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_get_port.assert_called_once_with(device="amigo")
        mock_is_port_working.assert_called_once_with("/mock/path0")
        mock_process_flash.assert_called_once_with(port="/mock/path0", callback=None)

    @patch("os.path.exists", return_value=True)
    @patch(
        "src.utils.flasher.flasher.Flasher.get_port",
        return_value=MagicMock(device="/mock/path0"),
    )
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.flasher.flasher.Flasher.process_flash")
    def test_flash_amigo_callback(
        self, mock_process_flash, mock_is_port_working, mock_get_port, mock_exists
    ):
        callback = MagicMock()
        f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
        f.flash(device="amigo", callback=callback)
        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_get_port.assert_called_once_with(device="amigo")
        mock_is_port_working.assert_called_once_with("/mock/path0")
        mock_process_flash.assert_called_once_with(
            port="/mock/path0", callback=callback
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.flasher.Flasher.get_port", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch(
        "src.utils.flasher.flasher.Flasher.process_flash",
        side_effect=Exception("Greeting fail: mock test"),
    )
    @patch("src.utils.flasher.flasher.Flasher.process_exception")
    # pylint: disable=too-many-arguments
    def test_flash_amigo_greeting_fail_no_callback(
        self,
        mock_process_exception,
        mock_process_flash,
        mock_is_port_working,
        mock_get_port,
        mock_exists,
    ):
        with self.assertRaises(Exception) as exc_info:
            f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
            f.flash(device="amigo")
            mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
            mock_get_port.assert_called_once_with(device="amigo")
            mock_is_port_working.assert_called_once_with("/mock/path0")
            mock_process_flash.assert_called_once_with(
                port="/mock/path0", callback=None
            )
            mock_process_exception.assert_called_once_with(
                oldport="/mock/path0",
                exc_info=exc_info.exception,
                process=f.process_flash,
                callback=None,
            )

    @patch("os.path.exists", return_value=True)
    @patch(
        "src.utils.flasher.flasher.Flasher.get_port",
        return_value=MagicMock(device="/mock/path0"),
    )
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=False)
    def test_fail_flash_amigo(self, mock_is_port_working, mock_get_port, mock_exists):
        with self.assertRaises(RuntimeError) as exc_info:
            f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
            f.flash(device="amigo")
            mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
            mock_get_port.assert_called_once_with(device="amigo")
            mock_is_port_working.assert_called_once_with("/mock/path0")
        self.assertEqual(str(exc_info.exception), "Port not working: /mock/path0")
