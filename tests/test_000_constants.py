import os
from unittest import TestCase
from unittest.mock import mock_open, patch, MagicMock
from src.utils.constants import _open_pyproject, get_name, get_version, get_description

# Updated to use [project] instead of [tool.poetry]
PYPROJECT_STR = """[project]
name = "test"
version = "0.0.1"
description = "Hello World!\""""

MOCK_TOML_DATA = {
    "project": {"name": "test", "version": "0.0.1", "description": "Hello World!"}
}


class TestConstants(TestCase):

    @patch("sys.version_info")
    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_STR)
    def test_open_pyproject_with_py_minor_version_10(
        self, open_mock, mock_version_info
    ):
        mock_version_info.minor = 9
        mock_tomli = MagicMock()
        mock_tomli.loads.return_value = MOCK_TOML_DATA

        with patch.dict("sys.modules", {"tomli": mock_tomli}):
            rootdirname = os.path.abspath(os.path.dirname(__file__))
            pyproject_filename = os.path.abspath(
                os.path.join(rootdirname, "..", "pyproject.toml")
            )

            data = _open_pyproject()
            open_mock.assert_called_once_with(pyproject_filename, "r", encoding="utf8")
            mock_tomli.loads.assert_called_once_with(PYPROJECT_STR.strip())
            self.assertEqual(data, MOCK_TOML_DATA)

    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_STR)
    def test_open_pyproject(self, open_mock):
        rootdirname = os.path.abspath(os.path.dirname(__file__))
        pyproject_filename = os.path.abspath(
            os.path.join(rootdirname, "..", "pyproject.toml")
        )

        data = _open_pyproject()
        open_mock.assert_called_once_with(pyproject_filename, "r", encoding="utf8")
        self.assertEqual(
            data,
            {
                "project": {
                    "name": "test",
                    "version": "0.0.1",
                    "description": "Hello World!",
                }
            },
        )

    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_STR)
    def test_fail_open_pyproject_file_not_found(self, open_mock):
        open_mock.side_effect = FileNotFoundError

        rootdirname = os.path.abspath(os.path.dirname(__file__))
        pyproject_filename = os.path.abspath(
            os.path.join(rootdirname, "..", "pyproject.toml")
        )

        with self.assertRaises(FileNotFoundError) as exc_info:
            _open_pyproject()

        self.assertEqual(str(exc_info.exception), f"{pyproject_filename} isnt found")

    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_STR)
    def test_fail_open_pyproject_value_error(self, open_mock):
        open_mock.side_effect = ValueError

        rootdirname = os.path.abspath(os.path.dirname(__file__))
        pyproject_filename = os.path.abspath(
            os.path.join(rootdirname, "..", "pyproject.toml")
        )

        with self.assertRaises(ValueError) as exc_info:
            _open_pyproject()

        self.assertEqual(
            str(exc_info.exception), f"{pyproject_filename} is not valid toml file"
        )

    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_STR)
    def test_get_name(self, open_mock):
        name = get_name()
        open_mock.assert_called_once()
        self.assertEqual(name, "test")

    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_STR)
    def test_get_version(self, open_mock):
        version = get_version()
        open_mock.assert_called_once()
        self.assertEqual(version, "0.0.1")

    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_STR)
    def test_007_ensure_get_correct_description(self, open_mock):
        description = get_description()
        open_mock.assert_called_once()
        self.assertEqual(description, "Hello World!")