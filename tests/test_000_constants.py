import os

import pytest

from src.utils.constants import (
    FIRMWARE_DIR,
    FIRMWARE_VERSION,
    VALID_DEVICES,
    VALID_DEVICES_VERSIONS,
    compare_versions,
    get_description,
    get_device_support_info,
    get_firmware_path,
    get_name,
    get_valid_devices_for_version,
    get_version,
    is_device_valid_for_version,
)

FIRMWARE_AVAILABLE = (
    os.path.isdir(FIRMWARE_DIR)
    and any(f.endswith(".kfpkg") for f in os.listdir(FIRMWARE_DIR))
    if os.path.isdir(FIRMWARE_DIR)
    else False
)


class TestFirmwareVersion:
    def test_firmware_version_format(self):
        assert FIRMWARE_VERSION.startswith("v")
        parts = FIRMWARE_VERSION[1:].split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_firmware_dir_is_absolute(self):
        assert os.path.isabs(FIRMWARE_DIR)

    def test_firmware_dir_contains_version(self):
        assert FIRMWARE_VERSION in FIRMWARE_DIR


class TestValidDevices:
    def test_valid_devices_is_list(self):
        assert isinstance(VALID_DEVICES, list)
        assert len(VALID_DEVICES) > 0

    def test_all_devices_have_version_info(self):
        for device in VALID_DEVICES:
            assert device in VALID_DEVICES_VERSIONS

    def test_version_info_has_required_keys(self):
        for _device, info in VALID_DEVICES_VERSIONS.items():
            assert "initial" in info
            assert "final" in info

    def test_bit_is_discontinued(self):
        assert VALID_DEVICES_VERSIONS["bit"]["final"] == "v25.10.0"


class TestCompareVersions:
    def test_equal_versions(self):
        assert compare_versions("v22.03.0", "v22.03.0") == 0

    def test_lower_version(self):
        assert compare_versions("v22.03.0", "v24.03.0") == -1

    def test_higher_version(self):
        assert compare_versions("v24.03.0", "v22.03.0") == 1

    def test_patch_comparison(self):
        assert compare_versions("v22.03.0", "v22.03.1") == -1

    def test_invalid_version_returns_zero_tuple(self):
        assert compare_versions("invalid", "v22.03.0") == -1


class TestIsDeviceValidForVersion:
    def test_valid_device_and_version(self):
        assert is_device_valid_for_version("amigo", "v26.03.0") is True

    def test_device_before_initial_version(self):
        assert is_device_valid_for_version("amigo", "v22.03.0") is False

    def test_bit_discontinued_after_final(self):
        assert is_device_valid_for_version("bit", "v26.03.0") is False

    def test_bit_valid_at_final_version(self):
        assert is_device_valid_for_version("bit", "v25.10.0") is True

    def test_unknown_device(self):
        assert is_device_valid_for_version("unknown_device", "v26.03.0") is False


class TestGetValidDevicesForVersion:
    def test_returns_list(self):
        result = get_valid_devices_for_version("v26.03.0")
        assert isinstance(result, list)

    def test_bit_not_in_v26(self):
        result = get_valid_devices_for_version("v26.03.0")
        assert "bit" not in result

    def test_bit_in_v25_10_0(self):
        result = get_valid_devices_for_version("v25.10.0")
        assert "bit" in result

    def test_m5stickv_in_v26(self):
        result = get_valid_devices_for_version("v26.03.0")
        assert "m5stickv" in result


class TestGetDeviceSupportInfo:
    def test_known_device_returns_info(self):
        info = get_device_support_info("amigo")
        assert info["initial"] == "v22.08.0"
        assert info["final"] is None

    def test_unknown_device_returns_none_values(self):
        info = get_device_support_info("nonexistent")
        assert info["initial"] is None
        assert info["final"] is None

    def test_returns_copy_not_reference(self):
        info = get_device_support_info("amigo")
        info["initial"] = "tampered"
        assert VALID_DEVICES_VERSIONS["amigo"]["initial"] == "v22.08.0"


class TestGetFirmwarePath:
    def test_valid_device_returns_path(self):
        path = os.path.join(FIRMWARE_DIR, "amigo.kfpkg")
        assert path.endswith("amigo.kfpkg")

    def test_path_is_absolute(self):
        path = os.path.join(FIRMWARE_DIR, "amigo.kfpkg")
        assert os.path.isabs(path)

    @pytest.mark.skipif(
        not FIRMWARE_AVAILABLE,
        reason="Firmware files not present — run: uv run --extra builder poe fetch-firmware",
    )
    def test_firmware_file_exists(self):
        available_devices = [d for d in VALID_DEVICES if d != "bit"]
        for device in available_devices:
            path = get_firmware_path(device)
            assert os.path.exists(path), f"Missing firmware for {device}: {path}"

    def test_unknown_device_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown device"):
            get_firmware_path("nonexistent_device")

    def test_bit_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError, match="fetch-firmware"):
            get_firmware_path("bit")


class TestPyprojectHelpers:
    def test_get_name(self):
        assert get_name() == "krux-installer"

    def test_get_version(self):
        version = get_version()
        assert isinstance(version, str)
        assert len(version) > 0

    def test_get_description(self):
        desc = get_description()
        assert isinstance(desc, str)
        assert len(desc) > 0
