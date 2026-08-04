import hashlib
import os
import shutil

import pytest

from src.utils.constants import (
    FIRMWARE_DIR,
    FIRMWARE_MANIFEST,
    FIRMWARE_VERSION,
    VALID_DEVICES,
    VALID_DEVICES_VERSIONS,
    FirmwareIntegrityError,
    compare_versions,
    get_description,
    get_device_support_info,
    get_firmware_path,
    get_name,
    get_valid_devices_for_version,
    get_version,
    is_device_valid_for_version,
    load_firmware_manifest,
    sha256_of_file,
    verify_firmware,
)

FIRMWARE_AVAILABLE = (
    os.path.isdir(FIRMWARE_DIR)
    and any(f.endswith(".kfpkg") for f in os.listdir(FIRMWARE_DIR))
    if os.path.isdir(FIRMWARE_DIR)
    else False
)

MANIFEST_AVAILABLE = os.path.isfile(os.path.join(FIRMWARE_DIR, FIRMWARE_MANIFEST))


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


class TestSha256OfFile:
    def test_matches_hashlib(self, tmp_path):
        target = tmp_path / "sample.bin"
        target.write_bytes(b"krux" * 40000)
        expected = hashlib.sha256(b"krux" * 40000).hexdigest()
        assert sha256_of_file(str(target)) == expected

    def test_digest_is_lowercase_hex(self, tmp_path):
        target = tmp_path / "sample.bin"
        target.write_bytes(b"\x00\xff")
        digest = sha256_of_file(str(target))
        assert len(digest) == 64
        assert digest == digest.lower()


@pytest.mark.skipif(
    not MANIFEST_AVAILABLE,
    reason="Firmware manifest not present — run: uv run --extra builder poe fetch-firmware",
)
class TestFirmwareManifest:
    def test_manifest_covers_every_available_kfpkg(self):
        manifest = load_firmware_manifest()
        for name in os.listdir(FIRMWARE_DIR):
            if name.endswith(".kfpkg"):
                assert name in manifest, f"{name} missing from {FIRMWARE_MANIFEST}"

    def test_manifest_hashes_are_valid_digests(self):
        for digest in load_firmware_manifest().values():
            assert len(digest) == 64
            assert all(c in "0123456789abcdef" for c in digest)

    def test_embedded_firmware_matches_manifest(self):
        for device in [d for d in VALID_DEVICES if d != "bit"]:
            verify_firmware(device, os.path.join(FIRMWARE_DIR, f"{device}.kfpkg"))

    def test_tampered_firmware_is_rejected(self, tmp_path):
        tampered = tmp_path / "amigo.kfpkg"
        shutil.copyfile(os.path.join(FIRMWARE_DIR, "amigo.kfpkg"), tampered)
        with open(tampered, "r+b") as tampered_file:
            tampered_file.seek(1024)
            tampered_file.write(b"\xde\xad\xbe\xef")

        with pytest.raises(FirmwareIntegrityError, match="integrity check failed"):
            verify_firmware("amigo", str(tampered))

    def test_truncated_firmware_is_rejected(self, tmp_path):
        truncated = tmp_path / "amigo.kfpkg"
        shutil.copyfile(os.path.join(FIRMWARE_DIR, "amigo.kfpkg"), truncated)
        with open(truncated, "r+b") as truncated_file:
            truncated_file.truncate(1024)

        with pytest.raises(FirmwareIntegrityError, match="integrity check failed"):
            verify_firmware("amigo", str(truncated))

    def test_device_absent_from_manifest_is_rejected(self):
        with pytest.raises(FirmwareIntegrityError, match="No SHA256 recorded"):
            verify_firmware("bit", os.path.join(FIRMWARE_DIR, "amigo.kfpkg"))


class TestFirmwareManifestMissing:
    def test_missing_manifest_raises(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.utils.constants.FIRMWARE_DIR", str(tmp_path))
        with pytest.raises(FirmwareIntegrityError, match="manifest not found"):
            load_firmware_manifest()

    def test_empty_manifest_raises(self, monkeypatch, tmp_path):
        (tmp_path / FIRMWARE_MANIFEST).write_text("", encoding="utf8")
        monkeypatch.setattr("src.utils.constants.FIRMWARE_DIR", str(tmp_path))
        with pytest.raises(FirmwareIntegrityError, match="empty or malformed"):
            load_firmware_manifest()

    def test_manifest_is_parsed_into_mapping(self, monkeypatch, tmp_path):
        (tmp_path / FIRMWARE_MANIFEST).write_text(
            "AABB1122  amigo.kfpkg\nccdd3344  dock.kfpkg\n", encoding="utf8"
        )
        monkeypatch.setattr("src.utils.constants.FIRMWARE_DIR", str(tmp_path))
        manifest = load_firmware_manifest()
        assert manifest == {"amigo.kfpkg": "aabb1122", "dock.kfpkg": "ccdd3344"}


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
