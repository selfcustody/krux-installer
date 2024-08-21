from unittest import TestCase
from unittest.mock import patch, mock_open
from src.utils.verifyer.sha256_check_verifyer import Sha256CheckVerifyer

MOCK_SHA = "64675a1afffaa7b2dcf85283e664d662e4b8741cf0638df873dafee3b6cf749b"


class TestSha256CheckVerifyerDownloader(TestCase):

    @patch("os.path.exists", return_value=True)
    def test_init(self, mock_exists):
        c = Sha256CheckVerifyer(filename="test.mock.sha256.txt")
        self.assertEqual(c.filename, "test.mock.sha256.txt")
        self.assertEqual(c.read_mode, "r")
        mock_exists.assert_called_once_with("test.mock.sha256.txt")

    @patch("os.path.exists", return_value=True)
    def test_fail_init(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            Sha256CheckVerifyer(filename="test.mock.txt")
            mock_exists.assert_called_once_with("test.mock.txt")

        self.assertEqual(
            str(exc_info.exception),
            "Invalid file: test.mock.txt do not assert with .*\\.sha256\\.txt",
        )

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_SHA)
    def test_load(self, open_mock, mock_exists):
        sha = Sha256CheckVerifyer(filename="test.mock.sha256.txt")
        sha.load()
        mock_exists.assert_called_once_with("test.mock.sha256.txt")
        open_mock.assert_called_once_with("test.mock.sha256.txt", "r", encoding="utf8")
        self.assertEqual(
            sha.data, "64675a1afffaa7b2dcf85283e664d662e4b8741cf0638df873dafee3b6cf749b"
        )
