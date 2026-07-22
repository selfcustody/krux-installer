# Krux Installer

[![Build](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml/badge.svg)](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/selfcustody/krux-installer/graph/badge.svg?token=T4LMZtPa5H)](https://codecov.io/gh/selfcustody/krux-installer)
[![created at](https://img.shields.io/github/created-at/selfcustody/krux-installer)](https://github.com/selfcustody/krux-installer/commit/5d177795fe3df380c54d424ccfd0f23fc7e62c41)
[![downloads](https://img.shields.io/github/downloads/selfcustody/krux-installer/total)](https://github.com/selfcustody/krux-installer/releases)
[![downloads (latest release)](https://img.shields.io/github/downloads/selfcustody/krux-installer/latest/total)](https://github.com/selfcustody/krux-installer/releases)
[![commits (since latest release)](https://img.shields.io/github/commits-since/selfcustody/krux-installer/latest/main)](https://github.com/qlrd/krux-installer/compare/main...develop)

Krux Installer is a GUI based tool to flash [Krux](https://github.com/selfcustody/krux)
without typing any command in terminal for [flash the firmware onto the device](https://selfcustody.github.io/krux/getting-started/installing/#flash-the-firmware-onto-the-device).

## Works offline

Since `v0.0.22`, Krux Installer runs **fully offline**. The Krux firmware
binaries are bundled inside the installer at build time, so it no longer
contacts GitHub at runtime — no internet connection is required to flash
your device.

### What changed

Earlier versions fetched the firmware over the network: the installer queried
GitHub for the available releases, let you pick a version, then downloaded,
verified and unzipped the assets before flashing. All of that runtime
networking has been removed. The installer no longer:

- checks your internet connection on startup;
- queries GitHub for the list of available firmware versions;
- downloads, verifies or unzips firmware assets on your machine.

Instead, each release ships with a single firmware version already embedded,
verified and unpacked inside the binary. The user flow is now simply:
**open the installer → select your device → flash**.

### Choosing a firmware version

Each release ships with a fixed firmware version embedded in the binary
(the current one is `v26.03.0`). To flash a different firmware version,
download the installer release that bundles it, or build from source with
your desired version (see [Firmware embedding (for developers)](/#firmware-embedding-for-developers)).

## Installing

[<img src="img/badge_github.png" alt="github releases page" width="186">](https://github.com/selfcustody/krux-installer/releases)

Available for:

- Linux:
  - Debian-like;
  - Fedora-like;
  - In the experimental phase, we have a nix flake for development.
- Windows;
- MacOS:
  - intel processors;
  - arm64 processors (M1/M2/M3/M4).
  
## Build from source

- [System setup](/#system-setup)
  - [Linux](/#linux)
  - [Windows](/#windows)
  - [MacOS](/#macos)
  - [Install UV](/#install-UV)
- [Download sources](/#download-sources)
- [Update code](/#update-code)
- [Developing](/#developing)
  
## System setup

Make sure you have python:

```bash
python --version
```

### Linux

Generally, all Linux come with python.

### Windows

Follow the instructions at [python.org](https://www.python.org/downloads/windows/)

### MacOS

Before installing `krux-installer` source code, you will need prepare the system:

#### Install `brew` package manager

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install latest python

```bash
brew install python
```

and add this line to your `~/.zshrc`:

```bash
alias python=python3
```

#### Ensure openssl have a correct link

Python's `ssl` module relies on OpenSSL for cryptographic operations.
Ensure that OpenSSL is installed on your system and is compatible with the
Python version you're using.

Since we expect that you're using the Python installed with Homebrew,
it's recommended to install OpenSSL through Homebrew if it's not already
installed:

```bash
brew install openssl
```

After installing OpenSSL, make sure it's linked correctly:

```bash
brew link --force openssl
```

This ensures that the OpenSSL libraries are available in the expected
locations that Python can find and use.

#### Patch your zshrc

Library paths on MacOS involves verifying that the environment variables and system
configurationsare correctyly set to find the necessary libraries, such as OpenSSL,
which is crucial for the `ssl` module in Python.

On MacOS, the dynamic linker tool `dyld` uses environment variabes to locate shared
libraries. The primary environment variable for specifying library paths is
`DYLD_LIBRARY_PATH`.

Adding the lines below to your `~/.zshrc` (or similar) the `DYLD_LIBRARY_PATH`
will be set each time you open a new terminal session (and therefore the OpenSSL
libraries `libcrypto.dylib` and `libssl.dylib` will can be found):

```bash
OPENSSL_MAJOR_VERSION=`openssl --version | awk '{ print $2}' | cut -d . -f1`
OPENSSL_FULL_VERSION=`openssl --version | awk ' { print $2}'`
export DYLD_LIBRARY_PATH="/opt/homebrew/Cellar/openssl@$OPENSSL_MAJOR_VERSION/$OPENSSL_FULL_VERSION/lib:$DYLD_LIBRARY_PATH"
```

### Install UV

Follow the steps to install UV on [https://docs.astral.sh/uv/reference/storage/]

## Download sources

Clone the repository:

```bash
git clone --recurse-submodules https://github.com/selfcustody/krux-installer.git
```

Install python dependencies:

```bash
uv sync
```

## Update code

If already cloned the repo without using `--recurse-submodules`,
use the command below to clone the needed submodules:

```bash
git submodule update --init
```

## Developing

Krux-Installer uses `poe` task manager for formatting, linting, tests,
coverage and build.

### See all available tasks

```bash
uv run poe
```

### Format code

```bash
uv run poe format
```

### Lint

```bash
uv run poe lint
```

### Test and coverage

```bash
uv run poe test
```

For systems without a window manager:

```bash
# Linux only
uv run poe test --no-xvfb
```

You can see all coverage results opening you browser and type
`file:///<folder>/krux-installer/htmlcov/index.html` (assuming
`folder` is where you placed the `krux-installer` project).

### Build for any Linux distribution

```bash
uv sync --extra builder
uv run poe fetch-firmware
uv run poe build-linux
```

### Build for MacOS

```bash
uv sync --extra builder
uv run poe fetch-firmware
uv run poe build-macos
```

### Build for Windows

```bash
uv sync --extra builder
uv run poe fetch-firmware
uv run poe build-win
```

It will export all project in a
[`one-file`](https://pyinstaller.org/en/stable/usage.html#cmdoption-F) binary:

- linux: `./dist/krux-installer`
- macOS: `./dist/krux-installer.app/Contents/MacOS/krux-installer`
- windows: `./dist/krux-installer.exe`

To more options see [.ci/create-spec.py](./.ci/create-spec.py) against the PyInstaller
[options](https://pyinstaller.org).

## Firmware embedding (for developers)

The installer ships with firmware binaries embedded at build time.
This section documents how the embedding pipeline works and how to
use locally built binaries for development or testing.

### Directory layout

```text
prebuild/
└── fetch_firmware.sh     # canonical script: download → verify → embed

.firmware_download/       # landing folder (gitignored)
├── krux-<version>.zip
├── krux-<version>.zip.sha256.txt
├── krux-<version>.zip.sig
└── selfcustody.pem

src/utils/firmware/       # packing folder (committed, embedded in the binary)
└── <version>/
    ├── amigo.kfpkg
    ├── bit.kfpkg          # not present in all releases
    ├── cube.kfpkg
    ├── dock.kfpkg
    ├── embed_fire.kfpkg
    ├── m5stickv.kfpkg
    ├── tzt.kfpkg
    ├── wonder_k.kfpkg
    ├── wonder_mv.kfpkg
    └── yahboom.kfpkg
```

The `.firmware_download/` landing folder holds the raw assets from GitHub
(zip, checksum, signature and public key). It is gitignored and can be
deleted after a successful build.

The `src/utils/firmware/<version>/` packing folder contains only the
extracted `.kfpkg` files — one per supported device. These are committed
to the repository and embedded into the installer binary by PyInstaller
at build time.

### Fetching official firmware

```bash
uv sync --extra builder
uv run poe fetch-firmware
```

This runs `prebuild/fetch_firmware.sh`, which:

1. Downloads the release zip, SHA256 checksum, ECDSA signature and
   `selfcustody.pem` from GitHub into `.firmware_download/`;
2. Verifies the SHA256 checksum (`sha256sum` on Linux, `shasum` on macOS);
3. Verifies the ECDSA signature with `openssl` (warns and continues if
   `openssl` is not available);
4. Extracts `kboot.kfpkg` for each supported device and saves it as
   `src/utils/firmware/<version>/<device>.kfpkg`.

Required tools in `PATH`: `curl`, `unzip`.
Optional (for full verification): `sha256sum`/`shasum`, `openssl`.

### Using locally built binaries (dev mode)

If you are developing Krux firmware and want to test your locally compiled
binaries with the installer, place your `.kfpkg` files directly into the
packing folder — no download step needed:

```text
src/utils/firmware/<version>/
├── amigo.kfpkg      ← your locally built binary
└── ...
```

The version directory must match the `FIRMWARE_VERSION` constant in
`src/utils/constants/__init__.py`. When running the installer from source
(`uv run poe dev`), it will pick up whatever `.kfpkg` files are present
in that folder.

> **Note:** locally built binaries are unsigned. The installer will still
> flash them correctly; only the pre-build verification step (`fetch_firmware.sh`)
> requires a valid signature. No signature is checked at flash time.

### Cleaning up

After building the installer, the landing folder is no longer needed:

```bash
rm -rf .firmware_download/
```

The packing folder (`src/utils/firmware/`) should be kept as-is if you
want to commit the firmware files for reproducible builds.
