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
from unittest.mock import patch
from src.utils.signer.base_signer import BaseSigner


class TestBaseSigner(TestCase):

    @patch("os.path.exists", return_value=True)
    def test_filename(self, mock_exists):
        s = BaseSigner(filename="mock.txt")
        mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(s.filename, "mock.txt")

    @patch("os.path.exists", return_value=False)
    def test_fail_filename(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            BaseSigner(filename="mock.txt")
            mock_exists.assert_called_once_with("mock.txt")

        self.assertEqual(str(exc_info.exception), "mock.txt do not exists")

    @patch("os.path.exists", return_value=True)
    def test_filehash(self, mock_exists):
        s = BaseSigner(filename="mock.txt")
        s.filehash = "5f98101992d1b411c05050dec665c16b1ddfd88aec9dd3ed55eefa046a3f4ab9"
        mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(
            s.filehash,
            "5f98101992d1b411c05050dec665c16b1ddfd88aec9dd3ed55eefa046a3f4ab9",
        )

    @patch("os.path.exists", return_value=True)
    def test_fail_filehash(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            s = BaseSigner(filename="mock.txt")
            s.filehash = (
                "5h98101992i1b411j05050klm665n16o1pqfd88rst9uv3wd55eefa046a3f4ab9"
            )
            mock_exists.assert_called_once_with("mock.txt")

        self.assertEqual(
            str(exc_info.exception),
            "Invalid hash: 5h98101992i1b411j05050klm665n16o1pqfd88rst9uv3wd55eefa046a3f4ab9",
        )
