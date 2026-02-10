import os
from unittest import TestCase
from unittest.mock import mock_open, patch, MagicMock
from src.utils.constants import (
    _open_pyproject,
    get_name,
    get_version,
    get_description,
    _parse_version,
    compare_versions,
    is_device_valid_for_version,
    get_valid_devices_for_version,
    get_device_support_info,
)

PYPROJECT_STR = """[tool.poetry]
name = "test"
version = "0.0.1"
description = "Hello World!"
"""

PYPROJECT_INVALID = """Not a valid TOML format"""

PYPROJECT_MISSING_KEYS = """[tool.poetry]
name = "test"
description = "Missing version key"
"""
description = "Hello World!\""""

MOCK_TOML_DATA = {
    "tool": {
        "poetry": {"name": "test", "version": "0.0.1", "description": "Hello World!"}
    },
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

            mock_tomli.loads.assert_called_once_with(PYPROJECT_STR)

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

    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_MISSING_KEYS)
    def test_missing_version_key(self, _open_mock):
        with self.assertRaises(KeyError):
            get_version()

    @patch("builtins.open", new_callable=mock_open, read_data=PYPROJECT_INVALID)
    def test_invalid_toml_format(self, _open_mock):
        with self.assertRaises(ValueError):
            _open_pyproject()


class TestVersionParsing(TestCase):
    def test_parse_version_valid(self):
        result = _parse_version("v22.03.0")
        self.assertEqual(result, (22, 3, 0))

    def test_parse_version_valid_double_digits(self):
        result = _parse_version("v25.11.0")
        self.assertEqual(result, (25, 11, 0))

    def test_parse_version_invalid_format(self):
        result = _parse_version("22.03.0")
        self.assertEqual(result, (0, 0, 0))

    def test_parse_version_invalid_string(self):
        result = _parse_version("invalid")
        self.assertEqual(result, (0, 0, 0))

    def test_parse_version_empty_string(self):
        result = _parse_version("")
        self.assertEqual(result, (0, 0, 0))


class TestCompareVersions(TestCase):
    def test_compare_versions_less_than(self):
        result = compare_versions("v22.03.0", "v24.03.0")
        self.assertEqual(result, -1)

    def test_compare_versions_greater_than(self):
        result = compare_versions("v24.03.0", "v22.03.0")
        self.assertEqual(result, 1)

    def test_compare_versions_equal(self):
        result = compare_versions("v24.03.0", "v24.03.0")
        self.assertEqual(result, 0)

    def test_compare_versions_different_months(self):
        result = compare_versions("v24.03.0", "v24.07.0")
        self.assertEqual(result, -1)

    def test_compare_versions_different_patches(self):
        result = compare_versions("v24.03.0", "v24.03.1")
        self.assertEqual(result, -1)

    def test_compare_versions_invalid_first(self):
        result = compare_versions("invalid", "v24.03.0")
        self.assertEqual(result, -1)

    def test_compare_versions_invalid_second(self):
        result = compare_versions("v24.03.0", "invalid")
        self.assertEqual(result, 1)

    def test_compare_versions_both_invalid(self):
        result = compare_versions("invalid1", "invalid2")
        self.assertEqual(result, 0)


class TestIsDeviceValidForVersion(TestCase):
    def test_device_valid_at_initial_version(self):
        result = is_device_valid_for_version("m5stickv", "v22.03.0")
        self.assertTrue(result)

    def test_device_valid_after_initial_version(self):
        result = is_device_valid_for_version("amigo", "v24.03.0")
        self.assertTrue(result)

    def test_device_invalid_before_initial_version(self):
        result = is_device_valid_for_version("yahboom", "v22.03.0")
        self.assertFalse(result)

    def test_device_valid_at_final_version(self):
        result = is_device_valid_for_version("bit", "v25.10.0")
        self.assertTrue(result)

    def test_device_invalid_after_final_version(self):
        result = is_device_valid_for_version("bit", "v25.11.0")
        self.assertFalse(result)

    def test_device_without_final_version(self):
        result = is_device_valid_for_version("m5stickv", "v99.99.0")
        self.assertTrue(result)

    def test_invalid_device(self):
        result = is_device_valid_for_version("nonexistent", "v24.03.0")
        self.assertFalse(result)

    def test_yahboom_valid_at_initial(self):
        result = is_device_valid_for_version("yahboom", "v24.03.0")
        self.assertTrue(result)

    def test_cube_valid_at_initial(self):
        result = is_device_valid_for_version("cube", "v24.07.0")
        self.assertTrue(result)

    def test_wonder_mv_valid_at_initial(self):
        result = is_device_valid_for_version("wonder_mv", "v24.09.0")
        self.assertTrue(result)

    def test_tzt_valid_at_initial(self):
        result = is_device_valid_for_version("tzt", "v25.10.0")
        self.assertTrue(result)

    def test_embed_fire_valid_at_initial(self):
        result = is_device_valid_for_version("embed_fire", "v25.11.0")
        self.assertTrue(result)

    def test_wonder_k_valid_at_initial(self):
        result = is_device_valid_for_version("wonder_k", "v25.11.0")
        self.assertTrue(result)


class TestGetValidDevicesForVersion(TestCase):
    def test_get_valid_devices_early_version(self):
        result = get_valid_devices_for_version("v22.03.0")
        self.assertIn("m5stickv", result)
        self.assertNotIn("amigo", result)
        self.assertNotIn("yahboom", result)

    def test_get_valid_devices_v22_08_0(self):
        result = get_valid_devices_for_version("v22.08.0")
        self.assertIn("m5stickv", result)
        self.assertIn("amigo", result)
        self.assertIn("dock", result)
        self.assertIn("bit", result)
        self.assertNotIn("yahboom", result)

    def test_get_valid_devices_v24_03_0(self):
        result = get_valid_devices_for_version("v24.03.0")
        self.assertIn("m5stickv", result)
        self.assertIn("amigo", result)
        self.assertIn("yahboom", result)
        self.assertNotIn("cube", result)

    def test_get_valid_devices_v24_07_0(self):
        result = get_valid_devices_for_version("v24.07.0")
        self.assertIn("cube", result)
        self.assertNotIn("wonder_mv", result)

    def test_get_valid_devices_v24_09_0(self):
        result = get_valid_devices_for_version("v24.09.0")
        self.assertIn("wonder_mv", result)
        self.assertIn("bit", result)

    def test_get_valid_devices_v25_10_0(self):
        result = get_valid_devices_for_version("v25.10.0")
        self.assertIn("tzt", result)
        self.assertIn("bit", result)
        self.assertNotIn("embed_fire", result)
        self.assertNotIn("wonder_k", result)

    def test_get_valid_devices_v25_11_0(self):
        result = get_valid_devices_for_version("v25.11.0")
        self.assertIn("embed_fire", result)
        self.assertIn("wonder_k", result)
        self.assertNotIn("bit", result)

    def test_get_valid_devices_future_version(self):
        result = get_valid_devices_for_version("v99.99.0")
        self.assertIn("m5stickv", result)
        self.assertIn("amigo", result)
        self.assertNotIn("bit", result)


class TestGetDeviceSupportInfo(TestCase):
    def test_get_device_support_info_m5stickv(self):
        result = get_device_support_info("m5stickv")
        self.assertEqual(result["initial"], "v22.03.0")
        self.assertIsNone(result["final"])

    def test_get_device_support_info_bit(self):
        result = get_device_support_info("bit")
        self.assertEqual(result["initial"], "v22.08.0")
        self.assertEqual(result["final"], "v25.10.0")

    def test_get_device_support_info_yahboom(self):
        result = get_device_support_info("yahboom")
        self.assertEqual(result["initial"], "v24.03.0")
        self.assertIsNone(result["final"])

    def test_get_device_support_info_embed_fire(self):
        result = get_device_support_info("embed_fire")
        self.assertEqual(result["initial"], "v25.11.0")
        self.assertIsNone(result["final"])

    def test_get_device_support_info_wonder_k(self):
        result = get_device_support_info("wonder_k")
        self.assertEqual(result["initial"], "v25.11.0")
        self.assertIsNone(result["final"])

    def test_get_device_support_info_invalid_device(self):
        result = get_device_support_info("nonexistent")
        self.assertIsNone(result["initial"])
        self.assertIsNone(result["final"])

    def test_get_device_support_info_returns_copy(self):
        result1 = get_device_support_info("m5stickv")
        result2 = get_device_support_info("m5stickv")
        self.assertIsNot(result1, result2)
        self.assertEqual(result1, result2)
