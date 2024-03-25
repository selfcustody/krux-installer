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
from unittest.mock import patch, mock_open, call
from src.utils.signer.trigger_signer import TriggerSigner


class TestTriggerSigner(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=b"Mocked")
    def test_make_hash(self, mocked_open, mock_exists):
        s = TriggerSigner(filename="mock.txt")
        s.make_hash()
        mock_exists.assert_called_once_with("mock.txt")
        mocked_open.assert_called_once_with("mock.txt", "rb")
        self.assertEqual(
            s.filehash,
            "28839e02daae61fae440d5e9617f6fd16a572f4e76c2e68566592fb902f74be5",
        )

    @patch("os.path.exists", return_value=True)
    def test_fail_save_hash(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            s = TriggerSigner(filename="mock.txt")
            s.save_hash()
            mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(str(exc_info.exception), "Empty hash")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=b"Mocked")
    @patch("builtins.print")
    def test_save_hash(self, mock_print, mocked_open, mock_exists):
        s = TriggerSigner(filename="mock.txt")
        s.make_hash()
        s.save_hash()
        mock_exists.assert_called_once_with("mock.txt")
        mocked_open.assert_has_calls(
            [
                call("mock.txt", "rb"),
                # pylint: disable=unnecessary-dunder-call
                call().__enter__(),
                call().read(),
                call().__exit__(None, None, None),
                call("mock.txt.sha256.txt", mode="w", encoding="utf-8"),
                # pylint: disable=unnecessary-dunder-call
                call().__enter__(),
                call().write(
                    "28839e02daae61fae440d5e9617f6fd16a572f4e76c2e68566592fb902f74be5 mock.txt"
                ),
                call().__exit__(None, None, None),
            ]
        )
        mock_print.assert_has_calls(
            [
                call(""),
                call("====================="),
                call("mock.txt.sha256.txt saved"),
                call("====================="),
                call(""),
            ]
        )

    @patch("os.path.exists", return_value=True)
    def test_fail_save_signature(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            s = TriggerSigner(filename="mock.txt")
            s.save_signature()
            mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(str(exc_info.exception), "Empty signature")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=b"Mocked")
    @patch("builtins.print")
    def test_save_signature(self, mock_print, mocked_open, mock_exists):
        s = TriggerSigner(filename="mock.txt")
        s.signature = "".join(
            [
                "MEQCIC2VjiRUu/UyjDlfQJCrA8Yy",
                "PE8gxqZXslsqck3N6t/2AiBj0hvV",
                "6lpczTW4CoaBGlmQB/0yKice5BUF",
                "6xwHQRWvow==",
            ]
        )
        s.save_signature()
        mock_exists.assert_called_once_with("mock.txt")
        mocked_open.assert_has_calls(
            [
                call("mock.txt.sig", "wb"),
                # pylint: disable=unnecessary-dunder-call
                call().__enter__(),
                # pylint: disable=line-too-long
                call().write(
                    b"0D\x02 -\x95\x8e$T\xbb\xf52\x8c9_@\x90\xab\x03\xc62<O \xc6\xa6W\xb2[*rM\xcd\xea\xdf\xf6\x02 c\xd2\x1b\xd5\xeaZ\\\xcd5\xb8\n\x86\x81\x1aY\x90\x07\xfd2*'\x1e\xe4\x15\x05\xeb\x1c\x07A\x15\xaf\xa3"
                ),
                call().__exit__(None, None, None),
            ]
        )
        mock_print.assert_has_calls(
            [
                call(""),
                call("====================="),
                call("mock.txt.sig saved"),
                call("====================="),
                call(""),
            ]
        )
