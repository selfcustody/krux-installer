# Pre-release workaround

How to flash-test the installer against firmware that has not been released
yet.

## The problem

`prebuild/fetch_firmware.sh` downloads `krux-<version>.zip` from
[selfcustody/krux releases][releases], checks its SHA256 and its ECDSA
signature against the committed `selfcustody.pem`, extracts one
`<device>.kfpkg` per device into `src/utils/firmware/<version>/`, and writes
`src/utils/firmware_hashes.py` — the table the app re-checks before flashing.

None of that exists during release preparation. The tag is not pushed, so the
zip, the `.sha256.txt` and the `.sig` all 404, and the script cannot get past
step 1. Meanwhile the installer itself has already been bumped: with
`FIRMWARE_VERSION = "v26.09.0"` in `src/utils/constants/__init__.py` and a
leftover `firmware_hashes.py` from the previous release, the flash screen
refuses:

```text
Firmware hashes were generated for v26.08.0, but this build expects v26.09.0.
Refusing to flash against a stale reference.
```

That check lives in `load_firmware_manifest()`
(`src/utils/constants/__init__.py`) and is doing its job — the two versions
genuinely disagree. But it leaves the release candidate impossible to test on
real hardware precisely when testing matters most.

## The workaround

`prebuild/generate_checksums.sh` stands in for the download-and-verify half of
`fetch_firmware.sh`, taking the firmware from a local Krux build tree instead:

```sh
KRUX_PATH=<path_to_krux_src> uv run poe generate-checksums --source $KRUX_PATH
```

The source is the directory holding `maixpy_<device>/kboot.kfpkg`, i.e. the
output of a local `krux` build. The version defaults to whatever
`src/utils/constants/__init__.py` expects, read at run time, so the generated
table cannot be stale against the app that reads it. Pass `--version` to
override.

It produces exactly what `fetch_firmware.sh` would: the same flat
`<device>.kfpkg` layout, the same `SHA256SUMS` in `sha256sum -c` format, and
the same `firmware_hashes.py` contract. Devices missing from the build are
warned about and skipped. The packing directory is wiped first, so a `.kfpkg`
left by an earlier version cannot survive into the table.

When the build tree ships a `build.txt` — the Krux build writes one, listing
the SHA256 of every artifact — the copies are cross-checked against it and the
run aborts on any mismatch. That catches a truncated or half-written copy,
which is the only failure this flow can actually detect.

Afterwards the installer flashes normally in dev mode.

## What it does not do

It does not verify anything, because at that point there is nothing to verify
against. No signed zip exists, so no signature is checked, and the digests
attest only that the files were copied intact out of a build tree you produced
yourself. Compare this with `--allow-unverified` on the real script, which
deliberately *refuses* to write `firmware_hashes.py` at all: it would rather
block the build than record hashes nobody vouched for.

This script writes that file anyway — that is the whole point of it, and the
reason it must not outlive the release candidate. `.ci/create-spec.py` only
checks that the module is present; it cannot tell a hand-made table from a
verified one. So a distributable installer built while this file is in place
would tell its users that the firmware matches its build-time hash, on the
authority of a local copy. The generated header says so, and the script prints
the same reminder when it finishes.

## Cleaning up

Once the release is tagged and published, throw the workaround away and let
the real script take over:

```sh
rm src/utils/firmware_hashes.py
uv run --extra builder poe fetch-firmware
```

`fetch_firmware.sh` overwrites the packing directory and the module wholesale,
so nothing hand-made survives. If the published release matches the build you
tested against, the digests come back identical — a useful last check that the
candidate and the release are the same firmware.

The script warns you if the release is already published, in which case you do
not need any of this.

[releases]: https://github.com/selfcustody/krux/releases
