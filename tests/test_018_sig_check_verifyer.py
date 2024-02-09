from unittest import TestCase
from unittest.mock import patch, mock_open
from src.utils.verifyer.sig_check_verifyer import SigCheckVerifyer

# pylint: disable=line-too-long
MOCK_SIG = b"0D\x02 8\x03&\xf5T\xa6\x08 #\xc0\x01\x02\xe5\xcb\xfe\xdd\xb3.\x86\xb6{W\x14\x9c\x04o\xf7m\xe5\x86T\xeb\x02 =\xb8\x9a\x83\x16\x1a\xe1R&\x14F\xab\x84\xceq\xcd\x1b\xacd\x15uI\xc4l\xd7X\x91\xdbq\xa6\xf8\xc0"


class TestPemCheckVerifyerDownloader(TestCase):

    @patch("os.path.exists", return_value=True)
    def test_init(self, mock_exists):
        s = SigCheckVerifyer(filename="test.mock.sig")
        self.assertEqual(s.filename, "test.mock.sig")
        self.assertEqual(s.read_mode, "rb")
        mock_exists.assert_called_once_with("test.mock.sig")

    @patch("os.path.exists", return_value=True)
    def test_fail_init(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            SigCheckVerifyer(filename="test.mock.txt")
            mock_exists.assert_called_once_with("test.mock.txt")

        self.assertEqual(
            str(exc_info.exception),
            "Invalid file: test.mock.txt do not assert with .*\\.sig",
        )

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_SIG)
    def test_load(self, open_mock, mock_exists):
        s = SigCheckVerifyer(filename="test.mock.sig")
        s.load()
        mock_exists.assert_called_once_with("test.mock.sig")
        open_mock.assert_called_once_with("test.mock.sig", "rb")
        self.assertEqual(
            s.data,
            b"0D\x02 8\x03&\xf5T\xa6\x08 #\xc0\x01\x02\xe5\xcb\xfe\xdd\xb3.\x86\xb6{W\x14\x9c\x04o\xf7m\xe5\x86T\xeb\x02 =\xb8\x9a\x83\x16\x1a\xe1R&\x14F\xab\x84\xceq\xcd\x1b\xacd\x15uI\xc4l\xd7X\x91\xdbq\xa6\xf8\xc0",
        )
