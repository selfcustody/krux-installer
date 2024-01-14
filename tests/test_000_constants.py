import os
from unittest import TestCase
from unittest.mock import mock_open
from unittest.mock import patch
from src.utils.constants import get_name, get_version, get_description

PYPROJECT_STR = "[tool.poetry]"
PYPROJECT_DICT = {
    "tool": {"poetry": {"name": "test", "version": "1", "description": "Hello World"}}
}


class TestConstants(TestCase):
    # pylint: disable=unused-argument
    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_STR)
    def test_000_ensure_get_pyproject_toml_is_read(self, pyproject_data_mock):
        root_dir = os.path.abspath(os.path.dirname(__file__))
        pyproject_filename = os.path.abspath(
            os.path.join(root_dir, "..", "..", "pyproject.toml")
        )
        with open(pyproject_filename, "rb") as pyproject_file_data:
            assert "[tool.poetry]" in pyproject_file_data.read()

    @patch("src.utils.constants._open_pyproject", return_value=PYPROJECT_DICT)
    def test_001_ensure_open_pyproject_is_called(self, _open_pyproject_mock):
        pyproject = _open_pyproject_mock()
        self.assertEqual(_open_pyproject_mock.call_count, 1)
        assert "tool" in pyproject
        assert "poetry" in pyproject["tool"]
        assert "name" in pyproject["tool"]["poetry"]

    @patch(
        "src.utils.constants.get_name",
        return_value=PYPROJECT_DICT["tool"]["poetry"]["name"],
    )
    def test_002_ensure_get_name_is_called(self, get_name_mock):
        name = get_name_mock()
        self.assertEqual(get_name_mock.call_count, 1)
        self.assertEqual(name, "test")

    def test_003_ensure_get_correct_name(self):
        name = get_name()
        self.assertEqual(name, "krux-installer")

    @patch(
        "src.utils.constants.get_version",
        return_value=PYPROJECT_DICT["tool"]["poetry"]["version"],
    )
    def test_004_ensure_get_version_is_called(self, get_version_mock):
        name = get_version_mock()
        self.assertEqual(get_version_mock.call_count, 1)
        self.assertEqual(name, "1")

    def test_005_ensure_get_correct_version(self):
        version = get_version()
        self.assertEqual(version, "0.0.2")

    @patch(
        "src.utils.constants.get_description",
        return_value=PYPROJECT_DICT["tool"]["poetry"]["description"],
    )
    def test_006_ensure_get_version_is_called(self, get_description_mock):
        name = get_description_mock()
        self.assertEqual(get_description_mock.call_count, 1)
        self.assertEqual(name, "Hello World")

    def test_007_ensure_get_correct_description(self):
        description = get_description()
        self.assertEqual(
            description,
            "A GUI based application to flash Krux firmware on K210 based devices",
        )
