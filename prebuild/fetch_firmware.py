#!/usr/bin/env python3
"""
scripts/fetch_firmware.py

Builder-only script: downloads, verifies and extracts Krux firmware binaries
for all supported devices into src/utils/firmware/<version>/.

Run with:
    uv run --extra builder python scripts/fetch_firmware.py

Requirements (builder extra only):
    requests, cryptography
"""

import hashlib
import os
import sys
import zipfile

try:
    import requests
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
except ImportError:
    print("ERROR: builder dependencies not installed.\nRun: uv sync --extra builder")
    sys.exit(1)

FIRMWARE_VERSION = "v26.03.0"
BASE_URL = f"https://github.com/selfcustody/krux/releases/download/{FIRMWARE_VERSION}"
ZIP_NAME = f"krux-{FIRMWARE_VERSION}.zip"
SHA256_NAME = f"{ZIP_NAME}.sha256.txt"
SIG_NAME = f"{ZIP_NAME}.sig"
PEM_NAME = "selfcustody.pem"
PEM_URL = "https://raw.githubusercontent.com/selfcustody/krux/main/selfcustody.pem"

# Devices whose folder inside the zip is maixpy_<device>
VALID_DEVICES = [
    "m5stickv",
    "amigo",
    "dock",
    "bit",
    "yahboom",
    "cube",
    "wonder_mv",
    "tzt",
    "embed_fire",
    "wonder_k",
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
FIRMWARE_DIR = os.path.join(ROOT_DIR, "src", "utils", "firmware", FIRMWARE_VERSION)
DOWNLOAD_DIR = os.path.join(ROOT_DIR, ".firmware_download")


def _download(url: str, dest: str) -> None:
    """Download a file from url to dest, skipping if already present."""
    if os.path.exists(dest):
        print(f"  [skip] {os.path.basename(dest)} already downloaded")
        return
    print(f"  [download] {url}")
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"  [ok] saved to {dest}")


def _verify_sha256(zip_path: str, sha256_path: str) -> None:
    """Verify SHA256 hash of zip file against the provided checksum file."""
    print("\n[verify] SHA256 checksum...")
    with open(sha256_path, "r", encoding="utf-8") as f:
        expected_hash = f.read().strip().split()[0].lower()

    sha256 = hashlib.sha256()
    with open(zip_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    actual_hash = sha256.hexdigest().lower()

    if actual_hash != expected_hash:
        raise ValueError(
            f"SHA256 mismatch!\n  expected: {expected_hash}\n  got:      {actual_hash}"
        )
    print(f"  [ok] SHA256 matches: {actual_hash}")


def _verify_signature(zip_path: str, sig_path: str, pem_path: str) -> None:
    """Verify the zip signature against selfcustody.pem public key."""
    print("\n[verify] Signature...")
    with open(pem_path, "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(), backend=default_backend()
        )
    with open(sig_path, "rb") as f:
        signature = f.read()
    with open(zip_path, "rb") as f:
        data = f.read()

    from cryptography.hazmat.primitives.asymmetric import ec, utils

    public_key.verify(
        signature,
        data,
        ec.ECDSA(hashes.SHA256()),
    )
    print("  [ok] Signature is valid")


def _extract_kfpkg(zip_path: str) -> None:
    """Extract kboot.kfpkg for each device into FIRMWARE_DIR."""
    print("\n[extract] kboot.kfpkg files...")
    os.makedirs(FIRMWARE_DIR, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        all_names = zf.namelist()

        for device in VALID_DEVICES:
            zip_entry = f"krux-{FIRMWARE_VERSION}/maixpy_{device}/kboot.kfpkg"

            if zip_entry not in all_names:
                print(
                    f"  [warn] no kboot.kfpkg found for device '{device}' — skipped (not in this release)"
                )
                continue

            dest_path = os.path.join(FIRMWARE_DIR, f"{device}.kfpkg")
            if os.path.exists(dest_path):
                print(f"  [skip] {device}.kfpkg already exists")
                continue

            with zf.open(zip_entry) as src, open(dest_path, "wb") as dst:
                dst.write(src.read())
            print(f"  [ok] extracted {device}.kfpkg")


def _write_gitkeep() -> None:
    """Ensure the firmware dir is tracked by git even when empty."""
    gitkeep = os.path.join(ROOT_DIR, "src", "utils", "firmware", ".gitkeep")
    if not os.path.exists(gitkeep):
        open(gitkeep, "w").close()


def main() -> None:
    print(f"=== Krux Firmware Fetcher — {FIRMWARE_VERSION} ===\n")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    zip_path = os.path.join(DOWNLOAD_DIR, ZIP_NAME)
    sha256_path = os.path.join(DOWNLOAD_DIR, SHA256_NAME)
    sig_path = os.path.join(DOWNLOAD_DIR, SIG_NAME)
    pem_path = os.path.join(DOWNLOAD_DIR, PEM_NAME)

    print("[step 1] Downloading assets...")
    _download(f"{BASE_URL}/{ZIP_NAME}", zip_path)
    _download(f"{BASE_URL}/{SHA256_NAME}", sha256_path)
    _download(f"{BASE_URL}/{SIG_NAME}", sig_path)
    _download(PEM_URL, pem_path)

    print("\n[step 2] Verifying integrity...")
    _verify_sha256(zip_path, sha256_path)
    _verify_signature(zip_path, sig_path, pem_path)

    print("\n[step 3] Extracting firmware...")
    _extract_kfpkg(zip_path)

    _write_gitkeep()

    print(
        f"\n=== Done! Firmware binaries are in src/utils/firmware/{FIRMWARE_VERSION}/ ==="
    )
    print(
        "You can now commit the firmware files and remove .firmware_download/ if desired."
    )


if __name__ == "__main__":
    main()
