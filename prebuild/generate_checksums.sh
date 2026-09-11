#!/usr/bin/env bash
# prebuild/generate_checksums.sh
#
# Packs LOCALLY BUILT Krux firmware into src/utils/firmware/<version>/ and
# writes the hash table the app checks before flashing.
#
# This is the deliberate kludge ("gambiarra") for the window before a
# release is tagged: prebuild/fetch_firmware.sh can only work once
# selfcustody/krux has published krux-<version>.zip together with its
# .sha256.txt and .sig, so during release preparation there is nothing signed
# to download and the installer cannot be exercised end to end. This script
# takes the place of the download+verify steps ONLY, reusing the same layout,
# the same SHA256SUMS format and the same firmware_hashes.py contract, so that
# what you test locally is byte-for-byte what fetch_firmware.sh would later
# produce from an identical release.
#
# What it does NOT do is verify anything. There is no signature to check, so
# the hash table it writes attests only that the files were copied intact out
# of a build tree you produced yourself. See pre-release-workaround.md.
#
# Usage:
#   bash prebuild/generate_checksums.sh --source <krux-build-dir> [--version vX.YY.Z]
#
# From the project root (recommended):
#   uv run poe generate-checksums --source ~/krux/krux-v26.09.0
#
# The source directory is a Krux build tree, i.e. the one holding
# maixpy_<device>/kboot.kfpkg. --version defaults to the FIRMWARE_VERSION the
# app expects, read from src/utils/constants/__init__.py, so the generated
# table always matches the build it is meant to satisfy.

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────────────
SOURCE_DIR=""
FIRMWARE_VERSION=""
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "${SCRIPT_DIR}")"
CONSTANTS_FILE="${ROOT_DIR}/src/utils/constants/__init__.py"

# ── Helpers ──────────────────────────────────────────────────────────────────

info()  { printf '  [ok]   %s\n' "$*"; }
warn()  { printf '  [warn] %s\n' "$*" >&2; }
skip()  { printf '  [skip] %s\n' "$*"; }
step()  { printf '\n[%s]\n' "$*"; }
die()   { printf '\nERROR: %s\n' "$*" >&2; exit 1; }

_sha256_of() {
    local file_path="$1"

    if command -v sha256sum &>/dev/null; then
        sha256sum "${file_path}" | awk '{print $1}' | tr '[:upper:]' '[:lower:]'
    elif command -v shasum &>/dev/null; then
        shasum -a 256 "${file_path}" | awk '{print $1}' | tr '[:upper:]' '[:lower:]'
    fi
}

# The version the app will check against. Reading it from the constants module
# rather than repeating it here means this script cannot generate a table that
# load_firmware_manifest() would reject as stale: that mismatch is the failure
# this workaround exists to get past, and hard-coding the version would just
# reintroduce it one file over.
_detect_version() {
    local detected
    detected=$(sed -n 's/^FIRMWARE_VERSION = "\(.*\)"$/\1/p' "${CONSTANTS_FILE}" | head -n 1)
    [[ -n "${detected}" ]] \
        || die "Could not read FIRMWARE_VERSION from ${CONSTANTS_FILE}.
Pass it explicitly with --version vX.YY.Z"
    printf '%s' "${detected}"
}

# If the release is already public, the real script is strictly better: it
# verifies a signature this one cannot. Best-effort only — no network, no
# curl, or a slow proxy must not break a local workflow.
_warn_if_released() {
    local version="$1"
    local url="https://github.com/selfcustody/krux/releases/download/${version}/krux-${version}.zip"
    local code

    command -v curl &>/dev/null || return 0
    code=$(curl -sI -o /dev/null -w '%{http_code}' --max-time 5 --location "${url}" 2>/dev/null) || return 0

    if [[ "${code}" == "200" ]]; then
        warn "${version} is PUBLISHED upstream — you do not need this workaround."
        warn "Run 'uv run --extra builder poe fetch-firmware' instead: it verifies"
        warn "the release signature, which this script cannot do."
    fi
}

# ── Packing ──────────────────────────────────────────────────────────────────

_copy_kfpkg() {
    local packing_dir="$1"

    # The source is inspected before anything is deleted: a typo in --source
    # used to empty the packing directory and only then report that the tree
    # held no firmware, destroying a working setup on a mistyped path.
    local device src_path dest_path
    local -a present=()
    for device in "${VALID_DEVICES[@]}"; do
        if [[ -f "${SOURCE_DIR}/maixpy_${device}/kboot.kfpkg" ]]; then
            present+=("${device}")
        else
            warn "no kboot.kfpkg for '${device}' in this build — skipped"
        fi
    done

    [[ "${#present[@]}" -gt 0 ]] \
        || die "No maixpy_<device>/kboot.kfpkg found under ${SOURCE_DIR}.
Is that really a Krux build tree? Nothing was changed."

    step "copy kboot.kfpkg files"
    mkdir -p "${packing_dir}"

    # Same reasoning as fetch_firmware.sh: wipe first, so what gets hashed can
    # only have come from the source tree named on this run. A leftover .kfpkg
    # from a previous version would otherwise be picked up by create-spec.py's
    # glob and by the hash table below.
    rm -f "${packing_dir}"/*.kfpkg "${packing_dir}/${MANIFEST_NAME}"

    for device in "${present[@]}"; do
        src_path="${SOURCE_DIR}/maixpy_${device}/kboot.kfpkg"
        dest_path="${packing_dir}/${device}.kfpkg"

        cp "${src_path}" "${dest_path}"
        info "copied ${device}.kfpkg -> ${dest_path}"
    done
}

# A Krux build writes build.txt next to the build tree with the SHA256 of every
# artifact it produced. When it is there, comparing against it catches a
# truncated or half-written copy — the only thing that can actually go wrong
# here, since nothing else in this flow is verified.
_cross_check_build_txt() {
    local packing_dir="$1"
    local build_txt=""
    local candidate

    for candidate in "${SOURCE_DIR}/build.txt" "$(dirname "${SOURCE_DIR}")/build.txt"; do
        if [[ -f "${candidate}" ]]; then
            build_txt="${candidate}"
            break
        fi
    done

    if [[ -z "${build_txt}" ]]; then
        skip "no build.txt found — copies not cross-checked"
        return
    fi

    step "cross-check against $(basename "$(dirname "${build_txt}")")/build.txt"

    local checked=0 device dest_path expected actual
    for device in "${VALID_DEVICES[@]}"; do
        dest_path="${packing_dir}/${device}.kfpkg"
        [[ -f "${dest_path}" ]] || continue

        expected=$(grep -E "^[0-9a-f]{64}  .*maixpy_${device}/kboot\.kfpkg$" "${build_txt}" \
            | awk '{print $1}' | head -n 1 || true)
        [[ -n "${expected}" ]] || continue

        actual=$(_sha256_of "${dest_path}")
        if [[ "${actual}" != "${expected}" ]]; then
            die "${device}.kfpkg does not match ${build_txt}!
  expected: ${expected}
  got:      ${actual}"
        fi
        checked=$((checked + 1))
    done

    if [[ "${checked}" -eq 0 ]]; then
        skip "build.txt has no kboot.kfpkg digests — copies not cross-checked"
    else
        info "${checked} file(s) match the build output"
    fi
}

_write_hashes() {
    local packing_dir="$1"
    local manifest="${packing_dir}/${MANIFEST_NAME}"
    local module="${ROOT_DIR}/${HASHES_MODULE}"

    if ! command -v sha256sum &>/dev/null && ! command -v shasum &>/dev/null; then
        die "sha256sum/shasum not found — cannot generate checksums."
    fi

    step "write ${MANIFEST_NAME} and ${HASHES_MODULE}"

    : > "${manifest}"

    # The header says plainly what this table is, because the file is otherwise
    # indistinguishable from the generated one and outlives the session that
    # made it. fetch_firmware.sh overwrites it wholesale, so a later real run
    # erases the warning along with the values it applies to.
    cat > "${module}" <<EOF
# Hand-written by prebuild/generate_checksums.sh — NOT a verified release.
#
# Digests below come from a local Krux build tree, copied before ${FIRMWARE_VERSION}
# was published, so no signature was ever checked. They exist so the installer
# can be exercised end to end during release preparation.
#
# Regenerate with 'uv run --extra builder poe fetch-firmware' once the release
# is tagged, and before building anything distributable.
# See pre-release-workaround.md.
"""firmware_hashes.py"""

FIRMWARE_VERSION = "${FIRMWARE_VERSION}"

FIRMWARE_SHA256 = {
EOF

    printf '\nDevice: SHA256 of .kfpkg file\n'
    local device dest_path hash
    for device in $(printf '%s\n' "${VALID_DEVICES[@]}" | sort); do
        dest_path="${packing_dir}/${device}.kfpkg"
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
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --source)
                [[ $# -ge 2 ]] || die "--source requires a directory"
                SOURCE_DIR="$2"
                shift 2
                ;;
            --version)
                [[ $# -ge 2 ]] || die "--version requires a value (e.g. v26.09.0)"
                FIRMWARE_VERSION="$2"
                shift 2
                ;;
            *)
                die "Unknown option: $1
Usage: bash prebuild/generate_checksums.sh --source <krux-build-dir> [--version vX.YY.Z]"
                ;;
        esac
    done

    [[ -n "${FIRMWARE_VERSION}" ]] || FIRMWARE_VERSION="$(_detect_version)"

    [[ -n "${SOURCE_DIR}" ]] \
        || die "--source is required: the Krux build tree holding maixpy_<device>/kboot.kfpkg
Example: bash prebuild/generate_checksums.sh --source ~/krux/krux-${FIRMWARE_VERSION}"

    SOURCE_DIR="${SOURCE_DIR/#\~/${HOME}}"
    [[ -d "${SOURCE_DIR}" ]] || die "Source directory not found: ${SOURCE_DIR}"
    SOURCE_DIR="$(cd "${SOURCE_DIR}" && pwd)"

    local packing_dir="${ROOT_DIR}/src/utils/firmware/${FIRMWARE_VERSION}"

    printf '=== Krux Local Checksum Generator — %s ===\n' "${FIRMWARE_VERSION}"
    warn "this is the pre-release workaround: nothing here is signature-verified"
    printf '  source: %s\n' "${SOURCE_DIR}"

    _warn_if_released "${FIRMWARE_VERSION}"

    _copy_kfpkg "${packing_dir}"
    _cross_check_build_txt "${packing_dir}"
    _write_hashes "${packing_dir}"
    _write_gitkeep

    printf '\n=== Done! ===\n'
    printf 'Firmware binaries are at:\n'
    printf '  %s/\n' "${packing_dir}"
    printf '\nThe installer will now flash %s in dev mode.\n' "${FIRMWARE_VERSION}"
    printf 'Before building anything distributable, replace this with a verified release:\n'
    printf '  rm %s\n' "${ROOT_DIR}/${HASHES_MODULE}"
    printf '  uv run --extra builder poe fetch-firmware\n'
}

main "$@"
