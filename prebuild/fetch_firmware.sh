#!/usr/bin/env bash
# prebuild/fetch_firmware.sh
#
# Downloads, verifies and extracts Krux firmware binaries for all supported
# devices into src/utils/firmware/<version>/.
#
# This script replaces the Python/requests-based prebuild/fetch_firmware.py
# for the download step. Signature verification still requires the
# cryptography Python package (uv sync --extra builder).
#
# Required tools (must be available in PATH):
#   curl     - download files
#   unzip    - extract firmware zip
#
# Optional tools (signature verification):
#   sha256sum  (Linux) or shasum (macOS) - SHA256 checksum verification
#   openssl    - ECDSA signature verification
#
# If sha256sum/shasum or openssl are not found, the script will warn and
# continue without that verification step.
#
# Usage:
#   bash prebuild/fetch_firmware.sh
#
# From the project root (recommended):
#   uv run poe fetch-firmware

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────────────

FIRMWARE_VERSION="v26.03.0"
BASE_URL="https://github.com/selfcustody/krux/releases/download/${FIRMWARE_VERSION}"
PEM_URL="https://raw.githubusercontent.com/selfcustody/krux/main/selfcustody.pem"

ZIP_NAME="krux-${FIRMWARE_VERSION}.zip"
SHA256_NAME="${ZIP_NAME}.sha256.txt"
SIG_NAME="${ZIP_NAME}.sig"
PEM_NAME="selfcustody.pem"

VALID_DEVICES=(
    "m5stickv"
    "amigo"
    "dock"
    "bit"
    "yahboom"
    "cube"
    "wonder_mv"
    "tzt"
    "embed_fire"
    "wonder_k"
)

# Paths relative to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "${SCRIPT_DIR}")"
LANDING_DIR="${ROOT_DIR}/.firmware_download"
PACKING_DIR="${ROOT_DIR}/src/utils/firmware/${FIRMWARE_VERSION}"

# ── Helpers ──────────────────────────────────────────────────────────────────

info()  { printf '  [ok]   %s\n' "$*"; }
warn()  { printf '  [warn] %s\n' "$*" >&2; }
skip()  { printf '  [skip] %s\n' "$*"; }
step()  { printf '\n[%s]\n' "$*"; }
die()   { printf '\nERROR: %s\n' "$*" >&2; exit 1; }

_require_cmd() {
    command -v "$1" &>/dev/null || die "'$1' not found in PATH. Please install it."
}

_download() {
    local url="$1"
    local dest="$2"
    local name
    name="$(basename "${dest}")"

    if [[ -f "${dest}" ]]; then
        skip "${name} already downloaded"
        return
    fi

    printf '  [download] %s\n' "${url}"
    curl --fail --silent --show-error --location --output "${dest}" "${url}" \
        || die "Failed to download ${url}"
    info "saved to ${dest}"
}

# ── Verification ─────────────────────────────────────────────────────────────

_verify_sha256() {
    local zip_path="$1"
    local sha256_path="$2"

    if command -v sha256sum &>/dev/null; then
        local checker="sha256sum"
    elif command -v shasum &>/dev/null; then
        local checker="shasum -a 256"
    else
        warn "sha256sum/shasum not found — skipping SHA256 verification"
        return
    fi

    step "verify SHA256 checksum"
    local expected
    expected=$(awk '{print $1}' "${sha256_path}" | tr '[:upper:]' '[:lower:]')

    local actual
    actual=$(${checker} "${zip_path}" | awk '{print $1}' | tr '[:upper:]' '[:lower:]')

    if [[ "${actual}" != "${expected}" ]]; then
        die "SHA256 mismatch!\n  expected: ${expected}\n  got:      ${actual}"
    fi
    info "SHA256 matches: ${actual}"
}

_verify_signature() {
    local zip_path="$1"
    local sig_path="$2"
    local pem_path="$3"

    if ! command -v openssl &>/dev/null; then
        warn "openssl not found — skipping ECDSA signature verification"
        warn "To enable signature verification, install openssl and re-run this script."
        return
    fi

    step "verify ECDSA signature"
    openssl dgst -sha256 -verify "${pem_path}" -signature "${sig_path}" "${zip_path}" \
        || die "Signature verification failed!"
    info "Signature is valid"
}

# ── Extraction ────────────────────────────────────────────────────────────────

_extract_kfpkg() {
    local zip_path="$1"

    step "extract kboot.kfpkg files"
    mkdir -p "${PACKING_DIR}"

    for device in "${VALID_DEVICES[@]}"; do
        local zip_entry="krux-${FIRMWARE_VERSION}/maixpy_${device}/kboot.kfpkg"
        local dest_path="${PACKING_DIR}/${device}.kfpkg"

        if [[ -f "${dest_path}" ]]; then
            skip "${device}.kfpkg already exists"
            continue
        fi

        # Check if entry exists inside the zip
        if ! unzip -l "${zip_path}" "${zip_entry}" &>/dev/null; then
            warn "no kboot.kfpkg for '${device}' in this release — skipped"
            continue
        fi

        unzip -p "${zip_path}" "${zip_entry}" > "${dest_path}" \
            || die "Failed to extract ${zip_entry}"
        info "extracted ${device}.kfpkg -> ${dest_path}"
    done
}

_write_gitkeep() {
    local gitkeep="${ROOT_DIR}/src/utils/firmware/.gitkeep"
    if [[ ! -f "${gitkeep}" ]]; then
        touch "${gitkeep}"
    fi
}

# ── Main ──────────────────────────────────────────────────────────────────────

main() {
    printf '=== Krux Firmware Fetcher — %s ===\n' "${FIRMWARE_VERSION}"

    _require_cmd curl
    _require_cmd unzip

    mkdir -p "${LANDING_DIR}"

    local zip_path="${LANDING_DIR}/${ZIP_NAME}"
    local sha256_path="${LANDING_DIR}/${SHA256_NAME}"
    local sig_path="${LANDING_DIR}/${SIG_NAME}"
    local pem_path="${LANDING_DIR}/${PEM_NAME}"

    step "step 1 — downloading assets"
    _download "${BASE_URL}/${ZIP_NAME}"    "${zip_path}"
    _download "${BASE_URL}/${SHA256_NAME}" "${sha256_path}"
    _download "${BASE_URL}/${SIG_NAME}"    "${sig_path}"
    _download "${PEM_URL}"                 "${pem_path}"

    step "step 2 — verifying integrity"
    _verify_sha256    "${zip_path}" "${sha256_path}"
    _verify_signature "${zip_path}" "${sig_path}" "${pem_path}"

    step "step 3 — extracting firmware"
    _extract_kfpkg "${zip_path}"

    _write_gitkeep

    printf '\n=== Done! ===\n'
    printf 'Firmware binaries are at:\n'
    printf '  %s/\n' "${PACKING_DIR}"
    printf '\nLanding files (zip + signatures) are at:\n'
    printf '  %s/\n' "${LANDING_DIR}"
    printf '\nYou can safely delete the landing folder after building:\n'
    printf '  rm -rf %s\n' "${LANDING_DIR}"
}

main "$@"