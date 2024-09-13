# Krux Installer

[![Build](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml/badge.svg)](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/selfcustody/krux-installer/graph/badge.svg?token=T4LMZtPa5H)](https://codecov.io/gh/selfcustody/krux-installer)
[![created at](https://img.shields.io/github/created-at/selfcustody/krux-installer)](https://github.com/selfcustody/krux-installer/commit/5d177795fe3df380c54d424ccfd0f23fc7e62c41)
[![downloads](https://img.shields.io/github/downloads/selfcustody/krux-installer/total)](https://github.com/selfcustody/krux-installer/releases)
[![downloads (latest release)](https://img.shields.io/github/downloads/selfcustody/krux-installer/latest/total)](https://github.com/selfcustody/krux-installer/releases)
[![commits (since latest release)](https://img.shields.io/github/commits-since/selfcustody/krux-installer/latest/main)](https://github.com/qlrd/krux-installer/compare/main...develop)

Krux Installer is a GUI based tool to flash [Krux](https://github.com/selfcustody/krux)
without typing any command in terminal for [flash the firmware onto the device](https://selfcustody.github.io/krux/getting-started/installing/#flash-the-firmware-onto-the-device).

## Installing

There are pre-built
[releases](https://github.com/selfcustody/krux-installer/releases) for:

* Linux:
  * Debian-like;
  * Fedora-like;
* Windows;
* MacOS:
  * intel processors;
  * arm64 processors (M1/M2/M3).
  
To build it from the source, please follow the steps below:

* [System setup](/#system-setup)
  * [Linux](/#linux)
  * [Windows](/#windows)
  * [MacOS](/#macos)
  * [Install poetry](/#install-poetry)
* [Download sources](/#download-sources)
* [Update code](/#update-code)
* [Developing](/#developing)
  
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

<details>
<summary>Install `brew` package manager</summary>

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

</details>

<details>
<summary>Install latest python</summary>

```bash
brew install python
```

and add this line to your `~/.zshrc`:

```bash
alias python=python3
```

</details>

<details>
<summary> Ensure openssl have a correct link</summary>

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
</details>

<details>
<summary>Patch your zshrc</summary>

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

</details>

### Install poetry

Make sure you have `poetry` installed:

```b̀ash
python -m pipx install poetry
````

If you have problems with installation, make sure to
properly [configure its options](https://pipx.pypa.io/latest/installation/#installation-options).

## Download sources

Clone the repository:

```bash
git clone --recurse-submodules https://github.com/krux-installer.git
```

Install python dependencies:

```b̀ash
poetry install
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

<details>
<summary>See all available tasks</summary>

```bash
poetry run poe
```

</details>

<details>
<summary>Format code</summary>

```bash
poetry run poe format
```

</details>

<details>
<summary>Lint</summary>

```bash
poetry run poe lint
```

</details>

<details>
<summary>Test and coverage</summary>

```bash
poetry run poe test
```

For systems without a window manager:

```bash
# Linux only
poetry run poe test --no-xvfb
```

You can see all coverage results opening you browser and type
`file:///<folder>/krux-installer/htmlcov/index.html` (assuming
`folder` is where you placed the `krux-installer` project).
</details>

<details>
<summary>Build for any Linux distribution</summary>

```bash
poetry run poe build-linux
```

</details>

<details>
<summary>Build for MacOS</summary>

```bash
poetry run poe build-macos
```

</details>

<details>
<summary>Build for Windows</summary>

```bash
poetry run poe build-win
```

It will export all project in a
[`one-file`](https://pyinstaller.org/en/stable/usage.html#cmdoption-F) binary:

* linux: `./dist/krux-installer`
* macOS: `./dist/krux-installer.app/Contents/MacOS/krux-installer`
* windows: `./dist/krux-installer.exe`

To more options see [.ci/create-spec.py](./.ci/create-spec.py) against the PyInstaller
[options](https://pyinstaller.org).
</details>
