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
from unittest.mock import patch, call, MagicMock
from src.utils.flasher import Wiper
from .shared_mocks import MockListPortsGrep


class TestWiper(TestCase):

    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    def test_wipe_success(
        self, mock_process, mock_is_port_working, mock_next, mock_list_ports
    ):
        f = Wiper()
        f.baudrate = 1500000
        f.wipe(device="amigo")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_called_once_with(mock_next().device)
        mock_process.assert_called_once()

    def test_fail_wipe_wrong_baudrate(self):
        with self.assertRaises(ValueError) as exc_info:
            f = Wiper()
            f.baudrate = 1234567

        self.assertEqual(str(exc_info.exception), "Invalid baudrate: 1234567")

    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    def test_wipe_after_first_greeting_fail(
        self,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
    ):
        mock_exception = Exception("Greeting fail: mock test")
        mock_process.side_effect = [mock_exception, True]
        mock_next.side_effect = [MagicMock(device="mocked")]
        mock_list_ports.grep.return_value.__next__.side_effect = [
            MagicMock(device="mocked_next")
        ]

        f = Wiper()
        f.baudrate = 1500000
        f.wipe(device="amigo")

        # patch assertions
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_has_calls(
            [
                call("mocked"),
                call("mocked_next"),
            ]
        )
        mock_process.assert_has_calls([call(), call()])

    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", return_value=False)
    @patch("src.utils.flasher.base_flasher.KTool.log")
    def test_fail_wipe_port_not_working(
        self, mock_ktool_log, mock_is_port_working, mock_next, mock_list_ports
    ):
        mock_next.return_value = MagicMock(device="mocked")

        f = Wiper()
        f.baudrate = 1500000
        f.wipe(device="amigo")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_has_calls(
            [
                call("mocked"),
            ],
            any_order=True,
        )
        mock_ktool_log.assert_called_once_with("Port mocked not working")

    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", side_effect=[True, False])
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.base_flasher.KTool.log")
    def test_fail_wipe_after_first_greeting_fail_port_not_working(
        self,
        mock_ktool_log,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
    ):
        mock_exception = Exception("Greeting fail: mock test")
        mock_process.side_effect = [mock_exception]
        mock_next.side_effect = [MagicMock(device="mocked")]
        mock_list_ports.grep.return_value.__next__.side_effect = [
            MagicMock(device="mocked_next"),
        ]

        f = Wiper()
        f.baudrate = 1500000
        f.wipe(device="amigo")

        # patch assertions
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_has_calls(
            [
                call("mocked"),
                call("mocked_next"),
            ]
        )
        mock_process.assert_called_once()
        mock_ktool_log.assert_has_calls([call("Port mocked_next not working")])

    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.wiper.Wiper.is_port_working", side_effect=[True, True])
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.base_flasher.KTool.log")
    def test_fail_wipe_after_first_greeting_fail_stop_iteration(
        self,
        mock_ktool_log,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
    ):
        mock_exception = Exception("Greeting fail: mock test")
        mock_process.side_effect = [mock_exception, True]
        mock_next.side_effect = [MagicMock(device="mocked")]
        mock_list_ports.grep.return_value.__next__.side_effect = [
            StopIteration("mocked stop")
        ]

        f = Wiper()
        f.baudrate = 1500000
        f.wipe(device="amigo")

        # patch assertions
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_has_calls(
            [
                call("mocked"),
            ]
        )
        # mock_process.assert_called_once()
        mock_ktool_log.assert_has_calls([call("mocked stop")])
