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
from unittest.mock import patch, call
from src.utils.flasher import Wiper
from .shared_mocks import MockListPorts, MockSerial


class TestFlasher(TestCase):

    @patch("sys.platform", "linux")
    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_wipe_linux(self, mock_process, mock_list_ports, mock_exists):
        f = Wiper()
        f.wipe()

        mock_process.assert_called_once()
        mock_exists.assert_has_calls(
            [
                call("/mock/path"),
                call("/mock/path"),
            ]
        )

    @patch("sys.platform", "linux")
    @patch("os.path.exists", return_value=False)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_fail_wipe_unix(self, mock_process, mock_list_ports, mock_exists):
        with self.assertRaises(RuntimeError) as exc_info:
            f = Wiper()
            f.wipe()

            mock_process.assert_called_once()
            mock_exists.assert_has_calls(
                [
                    call("/mock/path"),
                    call("/mock/path"),
                ]
            )
        self.assertEqual(str(exc_info.exception), "Port do not exist: /mock/path")

    @patch("sys.platform", "darwin")
    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_wiper_darwin(self, mock_process, mock_list_ports, mock_exists):
        f = Wiper()
        f.wipe()

        mock_process.assert_called_once()
        mock_exists.assert_has_calls(
            [
                call("/mock/path"),
                call("/mock/path"),
            ]
        )

    @patch("sys.platform", "win32")
    @patch("src.utils.flasher.base_flasher.Serial", side_effect=MockSerial)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_wiper_win(self, mock_process, mock_list_ports, mock_serial):
        f = Wiper()
        f.wipe()

        mock_process.assert_called_once()
