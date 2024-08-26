import tempfile
import zipfile
from unittest import TestCase
from unittest.mock import patch, call, mock_open
from src.utils.unzip.base_unzip import BaseUnzip
from .shared_mocks import PropertyInstanceMock, MockZipFile


class TestBaseUnzip(TestCase):

    @patch("os.path.exists", return_value=True)
    def test_init(self, mock_exists):
        unzip = BaseUnzip(filename="test.zip", members=["README.md"])
        mock_exists.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        self.assertEqual(unzip.filename, "test.zip")
        self.assertIn("README.md", unzip.members)
        self.assertEqual(unzip.output, tempfile.gettempdir())

    @patch("os.path.exists", side_effect=[True, False])
    def test_fail_init_not_exists(self, mock_exist):
        with self.assertRaises(ValueError) as exc_info:
            BaseUnzip(filename="test.zip", members=["README.md"])
            mock_exist.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        self.assertEqual(
            str(exc_info.exception), f"Given path not exist: {tempfile.gettempdir()}"
        )

    @patch("src.utils.unzip.base_unzip.ZipFile")
    @patch("os.path.exists", return_value=True)
    def test_fail_init_empty_zip(self, mock_exists, mock_zipfile):

        with self.assertRaises(ValueError) as exc_info:
            BaseUnzip(filename="test.zip", members=[])
            mock_exists.assert_has_calls(
                [call("test.zip"), call(tempfile.gettempdir())]
            )
            mock_zipfile.assert_called_once_with("test.zip", "r")
        self.assertEqual(str(exc_info.exception), "Members cannot be empty")

    @patch(
        "src.utils.unzip.base_unzip.BaseUnzip.members",
        new_callable=PropertyInstanceMock,
    )
    @patch("os.path.exists", return_value=True)
    def test_members(self, mock_exists, mock_members):
        unzip = BaseUnzip(filename="test.zip", members=["README.md"])
        mock_exists.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        mock_members.assert_called_once_with(unzip, ["README.md"])

    @patch(
        "src.utils.unzip.base_unzip.BaseUnzip.members",
        new_callable=PropertyInstanceMock,
    )
    @patch("os.path.exists", return_value=True)
    def test_output(self, mock_exists, mock_members):
        unzip = BaseUnzip(filename="test.zip", members=["README.md"])
        mock_exists.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        mock_members.assert_called_once_with(unzip, ["README.md"])

    @patch("src.utils.unzip.base_unzip.ZipFile")
    @patch("os.path.exists", return_value=True)
    def test_load_extract(self, mock_exists, mock_zipfile):
        mock_zipfile.return_value = MockZipFile()
        mock_zipfile.return_value.open = mock_open

        with patch.object(MockZipFile, "extract") as mock_extract:
            unzip = BaseUnzip(filename="test.zip", members=["README.md"])
            mock_exists.assert_has_calls(
                [call("test.zip"), call(tempfile.gettempdir())]
            )
            unzip.load()
            mock_extract.assert_called_once_with(
                "README.md", path=tempfile.gettempdir()
            )

    @patch("src.utils.unzip.base_unzip.ZipFile")
    @patch("os.path.exists", return_value=True)
    def test_fail_load_badfile(self, mock_exists, mock_zipfile):

        mock_zipfile.side_effect = zipfile.BadZipfile

        with self.assertRaises(RuntimeError) as exc_info:
            unzip = BaseUnzip(filename="test.zip", members=["README.md"])
            mock_exists.assert_has_calls(
                [call("test.zip"), call(tempfile.gettempdir())]
            )

            unzip.load()
        self.assertEqual(str(exc_info.exception), "Cannot open test.zip: None")

    def test_sanitized_base_name(self):
        path = f"{tempfile.gettempdir()}/test/mock.zip"
        sanitized = BaseUnzip.sanitized_base_name(path)
        self.assertEqual(sanitized, "mock")
