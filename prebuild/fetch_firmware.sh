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
#   curl       - download files
#   unzip      - extract firmware zip
#   sha256sum  (Linux) or shasum (macOS) - SHA256 checksum verification
#   openssl    - ECDSA signature verification
#
# Verification fails closed: if sha256sum/shasum or openssl are missing the
# script aborts. Pass --allow-unverified to downgrade that to a warning and
# continue without the affected verification step.
#
# After extraction, each device's kboot.kfpkg SHA256 is printed in the same
# "device: hash" format as selfcustody/krux's reproducibility.py, so the
# embedded binaries can be cross-checked against independently reproduced
# builds. The same hashes are also generated into src/utils/firmware_hashes.py,
# which the app re-checks before flashing — the build-time proof would
# otherwise stop here and never reach the user running the packaged app.
#
# Usage:
#   bash prebuild/fetch_firmware.sh [--allow-unverified]
#
# From the project root (recommended):
#   uv run poe fetch-firmware [--allow-unverified]

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────────────
ALLOW_UNVERIFIED=0
FIRMWARE_VERSION="v26.08.0"
BASE_URL="https://github.com/selfcustody/krux/releases/download/${FIRMWARE_VERSION}"
PEM_URL="https://raw.githubusercontent.com/selfcustody/krux/main/selfcustody.pem"
ZIP_NAME="krux-${FIRMWARE_VERSION}.zip"
SHA256_NAME="${ZIP_NAME}.sha256.txt"
SIG_NAME="${ZIP_NAME}.sig"
PEM_NAME="selfcustody.pem"
MANIFEST_NAME="SHA256SUMS"
HASHES_MODULE="src/utils/firmware_hashes.py"
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

# Since the 2026 Coldcard incident, some users may want to verify everything
# themselves but lack a full OS setup with the required tools. We do not
# recommend --allow-unverified, but you can run it locally with
# `uv run poe fetch-firmware --allow-unverified` if you find yourself in
# trouble and do not know what to do. Any attempt to add --allow-unverified
# to CI (e.g. via a PR) will be CLOSED.
_missing_tool() {
    local tool="$1"
    local what="$2"

    if [[ "${ALLOW_UNVERIFIED}" -eq 1 ]]; then
        warn "${tool} not found — skipping ${what} (--allow-unverified)"
        return 0
    fi
    die "${tool} not found — refusing to continue without ${what}.
Install ${tool}, or re-run with --allow-unverified to skip this check."
}

_sha256_of() {
    local file_path="$1"

    if command -v sha256sum &>/dev/null; then
        sha256sum "${file_path}" | awk '{print $1}' | tr '[:upper:]' '[:lower:]'
    elif command -v shasum &>/dev/null; then
        shasum -a 256 "${file_path}" | awk '{print $1}' | tr '[:upper:]' '[:lower:]'
    fi
}

_verify_sha256() {
    local zip_path="$1"
    local sha256_path="$2"

    if ! command -v sha256sum &>/dev/null && ! command -v shasum &>/dev/null; then
        _missing_tool "sha256sum/shasum" "SHA256 verification"
        return
    fi

    step "verify SHA256 checksum"
    local expected
    expected=$(awk '{print $1}' "${sha256_path}" | tr '[:upper:]' '[:lower:]')

    local actual
    actual=$(_sha256_of "${zip_path}")

    if [[ "${actual}" != "${expected}" ]]; then
        die "SHA256 mismatch!
  expected: ${expected}
  got:      ${actual}"
    fi
    info "SHA256 matches: ${actual}"
}

_verify_signature() {
    local zip_path="$1"
    local sig_path="$2"
    local pem_path="$3"

    if ! command -v openssl &>/dev/null; then
        _missing_tool "openssl" "ECDSA signature verification"
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

    _kfpkg_hashes
}

_kfpkg_hashes() {
    if ! command -v sha256sum &>/dev/null && ! command -v shasum &>/dev/null; then
        _missing_tool "sha256sum/shasum" "kfpkg SHA256 report"
        return
    fi

    # Hashes are captured only after the zip's SHA256 and ECDSA signature have
    # been verified, so every value below descends from a release proven
    # authentic at build time. They are written to two places:
    #
    #   1. SHA256SUMS next to the .kfpkg files — plain `sha256sum -c` input,
    #      for auditing the source tree by hand:
    #        cd src/utils/firmware/<version> && sha256sum -c SHA256SUMS
    #      This file is NOT embedded into the bundle and is NOT trusted at
    #      runtime.
    #
    #   2. src/utils/firmware_hashes.py — the reference the app actually
    #      checks against before flashing. It has to be Python source rather
    #      than a data file: we build --onefile on all three platforms, so
    #      pure-Python modules stay in the PYZ archive inside the executable
    #      and are imported from there, while --add-data files are unpacked
    #      to a temporary directory. A data-file manifest would sit in that
    #      same writable temp dir as the .kfpkg files it vouches for, and
    #      anything able to rewrite one could rewrite the other.
    local manifest="${PACKING_DIR}/${MANIFEST_NAME}"
    local module="${ROOT_DIR}/${HASHES_MODULE}"
    : > "${manifest}"

    cat > "${module}" <<EOF
# Generated by prebuild/fetch_firmware.sh — do not edit by hand.
#
# SHA256 of every embedded <device>.kfpkg, captured after the release zip's
# SHA256 and ECDSA signature were verified against selfcustody's public key.
#
# This lives in Python source on purpose. With --onefile, pure-Python modules
# stay in the PYZ archive embedded in the executable and are never unpacked to
# the runtime temp directory, so these values cannot be rewritten by whatever
# could rewrite the extracted .kfpkg files.
"""firmware_hashes.py"""

FIRMWARE_VERSION = "${FIRMWARE_VERSION}"

FIRMWARE_SHA256 = {
EOF

    printf '\nDevice: SHA256 of .kfpkg file\n'
    local device dest_path hash
    for device in $(printf '%s\n' "${VALID_DEVICES[@]}" | sort); do
        dest_path="${PACKING_DIR}/${device}.kfpkg"
        [[ -f "${dest_path}" ]] || continue
        hash=$(_sha256_of "${dest_path}")
        printf '%s: %s\n' "${device}" "${hash}"
        printf '%s  %s.kfpkg\n' "${hash}" "${device}" >> "${manifest}"
        printf '    "%s.kfpkg": "%s",\n' "${device}" "${hash}" >> "${module}"
    done

    printf '}\n' >> "${module}"

    info "wrote ${manifest}"
    info "wrote ${module}"
}

_write_gitkeep() {
    local gitkeep="${ROOT_DIR}/src/utils/firmware/.gitkeep"
    if [[ ! -f "${gitkeep}" ]]; then
        touch "${gitkeep}"
    fi
}

# ── Main ──────────────────────────────────────────────────────────────────────

main() {
    local arg
    for arg in "$@"; do
        case "${arg}" in
            --allow-unverified) ALLOW_UNVERIFIED=1 ;;
            *) die "Unknown option: ${arg}
Usage: bash prebuild/fetch_firmware.sh [--allow-unverified]" ;;
        esac
    done

    printf '=== Krux Firmware Fetcher — %s ===\n' "${FIRMWARE_VERSION}"

    _require_cmd curl
    _require_cmd unzip

    if [[ "${ALLOW_UNVERIFIED}" -eq 1 ]]; then
        warn "--allow-unverified: missing verification tools will be skipped, not fatal. But remember what happened."
    fi

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
