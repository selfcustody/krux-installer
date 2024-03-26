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
from unittest.mock import patch, call, mock_open
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

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=b"Mocked")
    @patch("builtins.print")
    def test_print_hash(self, mock_print, mocked_open, mock_exists):
        s = CliSigner(filename="mock.txt")
        s.make_hash()
        s.print_hash()
        mock_exists.assert_called_once_with("mock.txt")
        mocked_open.assert_called_once_with("mock.txt", "rb")
        mock_print.assert_has_calls(
            [
                call("====================================================="),
                call("====================================================="),
                call(
                    "28839e02daae61fae440d5e9617f6fd16a572f4e76c2e68566592fb902f74be5"
                ),
                call(),
            ]
        )

    @patch("os.path.exists", return_value=True)
    def test_fail_print_hash(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            s = CliSigner(filename="mock.txt")
            s.print_hash()
            mock_exists.assert_called_once_with("mock.txt")

        self.assertEqual(str(exc_info.exception), "Empty hash")

    @patch("os.path.exists", return_value=True)
    def test_scan(self, mock_exists):
        s = CliSigner(filename="mock.txt")
        data = s.scan(device="tests/mock.png")
        mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(data, "mock")

    @patch("os.path.exists", return_value=True)
    def test_scan_signature(self, mock_exists):
        s = CliSigner(filename="mock.txt")
        s.make_signature(device="tests/signature.png")
        mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(
            s.signature,
            b"".join(
                [
                    b"0D\x02 -\x95\x8e$T\xbb\xf52\x8c9_@\x90\xab\x03\xc22<O ",
                    b"\xc6\xa6W\xb2[*rM\xcd\xea\xdf\xf6\x02 c:\x1b\xd5\xeaZ\\",
                    b"\xcd5\xb8\n\x86\x81\x18\xb9\x90\x07\xfd2*'\x1e\xe4\x15",
                    b"\x05\xeb\x1c\x07A\x15\xaf\xa3",
                ]
            ),
        )

    @patch("os.path.exists", return_value=True)
    def test_scan_pubkey(self, mock_exists):
        s = CliSigner(filename="mock.txt")
        s.make_pubkey(device="tests/pubkey.png")
        mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(
            s.pubkey,
            "MDYwEAYHKoZIzj0CAQYFK4EEAAoDIgACf76jq/eAGf9tpI1sI1kxsmcy+q907u2o8Kfl6zJHfCA=",
        )
