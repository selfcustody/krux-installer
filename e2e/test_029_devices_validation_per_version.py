"""
Complete test coverage for src/utils/constants.py with proper mocking
These tests will cover EVERY line highlighted in red in the screenshots
"""

from unittest.mock import patch, MagicMock
from src.utils.constants import (
    _parse_version,
    compare_versions,
    is_device_valid_for_version,
    get_valid_devices_for_version,
    get_device_support_info,
)


class TestParseVersionWithMocks:

    @patch("src.utils.constants.re.match")
    def test_parse_version_match_returns_tuple(self, mock_match):
        mock_match_obj = MagicMock()
        mock_match_obj.groups.return_value = ("24", "7", "0")
        mock_match.return_value = mock_match_obj

        result = _parse_version("v24.07.0")
        assert result == (24, 7, 0)
        mock_match.assert_called_once()

    @patch("src.utils.constants.re.match")
    def test_parse_version_match_returns_none(self, mock_match):
        mock_match.return_value = None

        result = _parse_version("invalid")
        assert result == (0, 0, 0)
        mock_match.assert_called_once()

    def test_parse_version_real_valid_format(self):
        result = _parse_version("v24.07.0")
        assert result == (24, 7, 0)

    def test_parse_version_real_invalid_format(self):
        result = _parse_version("invalid")
        assert result == (0, 0, 0)


class TestCompareVersionsWithMocks:

    @patch("src.utils.constants._parse_version")
    def test_compare_less_than_branch(self, mock_parse):
        mock_parse.side_effect = [(22, 3, 0), (24, 7, 0)]

        result = compare_versions("v22.03.0", "v24.07.0")
        assert result == -1
        assert mock_parse.call_count == 2

    @patch("src.utils.constants._parse_version")
    def test_compare_greater_than_branch(self, mock_parse):
        mock_parse.side_effect = [(24, 7, 0), (22, 3, 0)]

        result = compare_versions("v24.07.0", "v22.03.0")

        assert result == 1
        assert mock_parse.call_count == 2

    @patch("src.utils.constants._parse_version")
    def test_compare_equal_branch(self, mock_parse):
        mock_parse.side_effect = [(24, 7, 0), (24, 7, 0)]

        result = compare_versions("v24.07.0", "v24.07.0")

        assert result == 0
        assert mock_parse.call_count == 2

    def test_compare_versions_real_less_than(self):
        result = compare_versions("v22.03.0", "v24.07.0")
        assert result == -1

    def test_compare_versions_real_greater_than(self):
        result = compare_versions("v24.07.0", "v22.03.0")
        assert result == 1

    def test_compare_versions_real_equal(self):
        result = compare_versions("v24.07.0", "v24.07.0")
        assert result == 0


class TestIsDeviceValidForVersionWithMocks:

    @patch("src.utils.constants.VALID_DEVICES_VERSIONS", {})
    def test_device_not_in_dict(self):
        result = is_device_valid_for_version("fake_device", "v24.07.0")

        assert result is False

    @patch("src.utils.constants.compare_versions")
    @patch(
        "src.utils.constants.VALID_DEVICES_VERSIONS",
        {"test_device": {"initial": "v22.08.0", "final": None}},
    )
    def test_device_before_initial_version(self, mock_compare):
        mock_compare.return_value = -1

        result = is_device_valid_for_version("test_device", "v22.07.0")

        assert result is False
        mock_compare.assert_called_once_with("v22.07.0", "v22.08.0")

    @patch("src.utils.constants.compare_versions")
    @patch(
        "src.utils.constants.VALID_DEVICES_VERSIONS",
        {"test_device": {"initial": "v22.08.0", "final": "v25.10.0"}},
    )
    def test_device_after_final_version(self, mock_compare):
        mock_compare.side_effect = [0, 1]

        result = is_device_valid_for_version("test_device", "v25.11.0")

        assert result is False
        assert mock_compare.call_count == 2

    @patch("src.utils.constants.compare_versions")
    @patch(
        "src.utils.constants.VALID_DEVICES_VERSIONS",
        {"test_device": {"initial": "v22.08.0", "final": "v25.10.0"}},
    )
    def test_device_within_valid_range(self, mock_compare):
        mock_compare.side_effect = [0, 0]

        result = is_device_valid_for_version("test_device", "v24.07.0")

        assert result is True
        assert mock_compare.call_count == 2

    @patch("src.utils.constants.compare_versions")
    @patch(
        "src.utils.constants.VALID_DEVICES_VERSIONS",
        {"test_device": {"initial": "v22.08.0", "final": None}},
    )
    def test_device_no_final_version(self, mock_compare):
        mock_compare.return_value = 0

        result = is_device_valid_for_version("test_device", "v30.00.0")

        assert result is True
        mock_compare.assert_called_once()

    def test_device_real_not_in_dict(self):
        result = is_device_valid_for_version("nonexistent", "v24.07.0")
        assert result is False

    def test_device_real_before_initial(self):
        result = is_device_valid_for_version("amigo", "v22.07.0")
        assert result is False

    def test_device_real_after_final(self):
        result = is_device_valid_for_version("bit", "v25.11.0")
        assert result is False

    def test_device_real_valid_range(self):
        result = is_device_valid_for_version("bit", "v24.07.0")
        assert result is True


class TestGetValidDevicesForVersionWithMocks:

    @patch("src.utils.constants.is_device_valid_for_version")
    @patch("src.utils.constants.VALID_DEVICES", ["device1", "device2", "device3"])
    def test_loop_and_append(self, mock_is_valid):
        mock_is_valid.side_effect = [True, False, True]

        result = get_valid_devices_for_version("v24.07.0")

        assert result == ["device1", "device3"]
        assert mock_is_valid.call_count == 3

    @patch("src.utils.constants.is_device_valid_for_version")
    @patch("src.utils.constants.VALID_DEVICES", ["device1", "device2"])
    def test_loop_append_all(self, mock_is_valid):
        mock_is_valid.return_value = True

        result = get_valid_devices_for_version("v24.07.0")

        assert result == ["device1", "device2"]
        assert mock_is_valid.call_count == 2

    @patch("src.utils.constants.is_device_valid_for_version")
    @patch("src.utils.constants.VALID_DEVICES", ["device1", "device2"])
    def test_loop_append_none(self, mock_is_valid):
        mock_is_valid.return_value = False

        result = get_valid_devices_for_version("v20.00.0")

        assert not result
        assert mock_is_valid.call_count == 2

    def test_real_v22_03_0_only_m5stickv(self):
        result = get_valid_devices_for_version("v22.03.0")
        assert result == ["m5stickv"]

    def test_real_v22_08_0_multiple_devices(self):
        result = get_valid_devices_for_version("v22.08.0")
        assert "m5stickv" in result
        assert "amigo" in result
        assert "dock" in result
        assert "bit" in result


class TestGetDeviceSupportInfoWithMocks:

    @patch("src.utils.constants.VALID_DEVICES_VERSIONS", {})
    def test_device_not_in_dict_returns_none(self):
        result = get_device_support_info("nonexistent")

        assert result == {"initial": None, "final": None}

    @patch(
        "src.utils.constants.VALID_DEVICES_VERSIONS",
        {"test_device": {"initial": "v22.08.0", "final": "v25.10.0"}},
    )
    def test_device_in_dict_returns_copy(self):
        result = get_device_support_info("test_device")

        assert result == {"initial": "v22.08.0", "final": "v25.10.0"}

        result["initial"] = "modified"
        result2 = get_device_support_info("test_device")
        assert result2["initial"] == "v22.08.0"

    def test_real_m5stickv_info(self):
        result = get_device_support_info("m5stickv")
        assert result["initial"] == "v22.03.0"
        assert result["final"] is None

    def test_real_bit_info(self):
        result = get_device_support_info("bit")
        assert result["initial"] == "v22.08.0"
        assert result["final"] == "v25.10.0"

    def test_real_invalid_device(self):
        result = get_device_support_info("invalid_device")
        assert result["initial"] is None
        assert result["final"] is None


class TestEdgeCasesAndIntegration:

    def test_parse_version_various_formats(self):
        assert _parse_version("v22.03.0") == (22, 3, 0)
        assert _parse_version("v24.07.0") == (24, 7, 0)
        assert _parse_version("invalid") == (0, 0, 0)
        assert _parse_version("22.03.0") == (0, 0, 0)
        assert _parse_version("v22.03") == (0, 0, 0)
        assert _parse_version("") == (0, 0, 0)

    def test_compare_versions_all_branches(self):
        assert compare_versions("v22.03.0", "v24.07.0") == -1
        assert compare_versions("v24.07.0", "v22.03.0") == 1
        assert compare_versions("v24.07.0", "v24.07.0") == 0

    def test_device_lifecycle_integration(self):
        assert is_device_valid_for_version("bit", "v22.07.0") is False
        assert is_device_valid_for_version("bit", "v22.08.0") is True
        assert is_device_valid_for_version("bit", "v24.07.0") is True
        assert is_device_valid_for_version("bit", "v25.10.0") is True
        assert is_device_valid_for_version("bit", "v25.11.0") is False

    def test_version_timeline_progression(self):
        v22_03 = get_valid_devices_for_version("v22.03.0")
        v22_08 = get_valid_devices_for_version("v22.08.0")
        v25_11 = get_valid_devices_for_version("v25.11.0")

        assert len(v22_03) == 1
        assert len(v22_08) == 4
        assert "bit" not in v25_11
        assert "embed_fire" in v25_11
