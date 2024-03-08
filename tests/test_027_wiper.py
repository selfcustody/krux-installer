# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
base_flasher.py
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock
from src.utils.flasher import Wiper
from .shared_mocks import MockListPortsGrep


class TestWiper(TestCase):

    @patch("sys.platform", "linux")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch("src.utils.flasher.wiper.Wiper.process_wipe")
    def test_wipe_amigo_no_callback_linux(
        self, mock_process_wipe, mock_is_port_working
    ):
        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            f = Wiper()
            f.wipe(device="amigo")
            mock_get_port.assert_called_once_with(device="amigo")
            mock_is_port_working.assert_called_once_with("/mock/path0")
            mock_process_wipe.assert_called_once_with(port="/mock/path0", callback=None)

    @patch("sys.platform", "darwin")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch("src.utils.flasher.wiper.Wiper.process_wipe")
    def test_wipe_amigo_no_callback_darwin(
        self, mock_process_wipe, mock_is_port_working
    ):
        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            f = Wiper()
            f.wipe(device="amigo")
            mock_get_port.assert_called_once_with(device="amigo")
            mock_is_port_working.assert_called_once_with("/mock/path0")
            mock_process_wipe.assert_called_once_with(port="/mock/path0", callback=None)

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch("src.utils.flasher.wiper.Wiper.process_wipe")
    def test_wipe_amigo_no_callback_win32(
        self, mock_process_wipe, mock_is_port_working
    ):
        with patch("src.utils.flasher.wiper.Wiper.get_port") as mock_get_port:
            mock_get_port.return_value = MockListPortsGrep().devices[0]
            f = Wiper()
            f.wipe(device="amigo")
            mock_get_port.assert_called_once_with(device="amigo")
            mock_is_port_working.assert_called_once_with("MOCK0")
            mock_process_wipe.assert_called_once_with(port="MOCK0", callback=None)

    @patch("sys.platform", "linux")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch("src.utils.flasher.wiper.Wiper.process_wipe")
    def test_wipe_amigo_callback_linux(self, mock_process_wipe, mock_is_port_working):
        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            callback = MagicMock()
            f = Wiper()
            f.wipe(device="amigo", callback=callback)
            mock_get_port.assert_called_once_with(device="amigo")
            mock_is_port_working.assert_called_once_with("/mock/path0")
            mock_process_wipe.assert_called_once_with(
                port="/mock/path0", callback=callback
            )

    @patch("sys.platform", "darwin")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch("src.utils.flasher.wiper.Wiper.process_wipe")
    def test_wipe_amigo_callback_darwin(self, mock_process_wipe, mock_is_port_working):
        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            callback = MagicMock()
            f = Wiper()
            f.wipe(device="amigo", callback=callback)
            mock_get_port.assert_called_once_with(device="amigo")
            mock_is_port_working.assert_called_once_with("/mock/path0")
            mock_process_wipe.assert_called_once_with(
                port="/mock/path0", callback=callback
            )

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch("src.utils.flasher.wiper.Wiper.process_wipe")
    def test_wipe_amigo_callback_win32(self, mock_process_wipe, mock_is_port_working):
        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            callback = MagicMock()
            f = Wiper()
            f.wipe(device="amigo", callback=callback)
            mock_get_port.assert_called_once_with(device="amigo")
            mock_is_port_working.assert_called_once_with("MOCK0")
            mock_process_wipe.assert_called_once_with(port="MOCK0", callback=callback)

    @patch("sys.platform", "linux")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch(
        "src.utils.flasher.wiper.Wiper.process_wipe",
        side_effect=Exception("Greeting fail: mock test"),
    )
    @patch("src.utils.flasher.wiper.Wiper.process_exception")
    # pylint: disable=too-many-arguments
    def test_wipe_amigo_greeting_fail_no_callback_linux(
        self,
        mock_process_exception,
        mock_process_flash,
        mock_is_port_working,
    ):

        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            with self.assertRaises(Exception) as exc_info:
                f = Wiper()
                f.wipe(device="amigo")
                mock_get_port.assert_called_once_with(device="amigo")
                mock_is_port_working.assert_called_once_with("/mock/path0")
                mock_process_flash.assert_called_once_with(
                    port="/mock/path0", callback=None
                )
                mock_process_exception.assert_called_once_with(
                    oldport="/mock/path0",
                    exc_info=exc_info.exception,
                    process=f.process_wipe,
                    callback=None,
                )

    @patch("sys.platform", "darwin")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch(
        "src.utils.flasher.wiper.Wiper.process_wipe",
        side_effect=Exception("Greeting fail: mock test"),
    )
    @patch("src.utils.flasher.wiper.Wiper.process_exception")
    # pylint: disable=too-many-arguments
    def test_wipe_amigo_greeting_fail_no_callback_darwin(
        self,
        mock_process_exception,
        mock_process_flash,
        mock_is_port_working,
    ):

        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            with self.assertRaises(Exception) as exc_info:
                f = Wiper()
                f.wipe(device="amigo")
                mock_get_port.assert_called_once_with(device="amigo")
                mock_is_port_working.assert_called_once_with("/mock/path0")
                mock_process_flash.assert_called_once_with(
                    port="/mock/path0", callback=None
                )
                mock_process_exception.assert_called_once_with(
                    oldport="/mock/path0",
                    exc_info=exc_info.exception,
                    process=f.process_wipe,
                    callback=None,
                )

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch(
        "src.utils.flasher.wiper.Wiper.process_wipe",
        side_effect=Exception("Greeting fail: mock test"),
    )
    @patch("src.utils.flasher.wiper.Wiper.process_exception")
    # pylint: disable=too-many-arguments
    def test_wipe_amigo_greeting_fail_no_callback_win32(
        self,
        mock_process_exception,
        mock_process_flash,
        mock_is_port_working,
    ):

        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            with self.assertRaises(Exception) as exc_info:
                f = Wiper()
                f.wipe(device="amigo")
                mock_get_port.assert_called_once_with(device="amigo")
                mock_is_port_working.assert_called_once_with("MOCK0")
                mock_process_flash.assert_called_once_with(port="MOCK0", callback=None)
                mock_process_exception.assert_called_once_with(
                    oldport="MOCK0",
                    exc_info=exc_info.exception,
                    process=f.process_wipe,
                    callback=None,
                )

    @patch("sys.platform", "linux")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=False)
    def test_fail_wipe_amigo_linux(self, mock_is_port_working):
        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            with self.assertRaises(RuntimeError) as exc_info:
                f = Wiper()
                f.wipe(device="amigo")
                mock_get_port.assert_called_once_with(device="amigo")
                mock_is_port_working.assert_called_once_with("/mock/path0")
        self.assertEqual(str(exc_info.exception), "Port not working: /mock/path0")

    @patch("sys.platform", "darwin")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=False)
    def test_fail_wipe_amigo_darwin(self, mock_is_port_working):
        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            with self.assertRaises(RuntimeError) as exc_info:
                f = Wiper()
                f.wipe(device="amigo")
                mock_get_port.assert_called_once_with(device="amigo")
                mock_is_port_working.assert_called_once_with("/mock/path0")
        self.assertEqual(str(exc_info.exception), "Port not working: /mock/path0")

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=False)
    def test_fail_wipe_amigo_win32(self, mock_is_port_working):
        with patch(
            "src.utils.flasher.wiper.Wiper.get_port",
            return_value=MockListPortsGrep().devices[0],
        ) as mock_get_port:
            with self.assertRaises(RuntimeError) as exc_info:
                f = Wiper()
                f.wipe(device="amigo")
                mock_get_port.assert_called_once_with(device="amigo")
                mock_is_port_working.assert_called_once_with("MOCK0")
        self.assertEqual(str(exc_info.exception), "Port not working: MOCK0")
