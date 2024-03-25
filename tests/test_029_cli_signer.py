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
from src.utils.signer import CliSigner


class TestCliSigner(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("builtins.print")
    def test_print_scan_hash_message(self, mock_print, mock_exists):
        s = CliSigner(filename="mock.txt")
        s.print_scan_hash_message()
        mock_exists.assert_called_once_with("mock.txt")
        mock_print.assert_has_calls(
            [
                call("====================================================="),
                call("To sign this file with Krux: "),
                call(" (a) load a 12/24 words key with or without password;"),
                call(" (b) use the Sign->Message feature;"),
                call(" (c) and scan this QR code below."),
                call("====================================================="),
                call(""),
            ]
        )

    @patch("os.path.exists", return_value=True)
    @patch("builtins.input", return_value=True)
    @patch("builtins.print")
    def test_print_scan_signature_message(self, mock_print, mock_input, mock_exists):
        s = CliSigner(filename="mock.txt")
        s.print_scan_signature_message()
        mock_exists.assert_called_once_with("mock.txt")
        mock_input.assert_called_once_with("Press enter to scan signature")
        mock_print.assert_has_calls(
            [
                call(""),
                call("====================================================="),
                call("====================================================="),
                call(""),
            ]
        )

    @patch("os.path.exists", return_value=True)
    @patch("builtins.input", return_value=True)
    @patch("builtins.print")
    def test_print_scan_pubkey_message(self, mock_print, mock_input, mock_exists):
        s = CliSigner(filename="mock.txt")
        s.print_scan_pubkey_message()
        mock_exists.assert_called_once_with("mock.txt")
        mock_input.assert_called_once_with("Press enter to scan public key")
        mock_print.assert_has_calls(
            [
                call(""),
                call("====================================================="),
                call("====================================================="),
                call(""),
            ]
        )
