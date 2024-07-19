# Krux Installer

[![Build main branch](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/qlrd/krux-installer/tree/kivy/graph/badge.svg?token=KD41H20MYS)](https://codecov.io/gh/qlrd/krux-installer)
[![created at](https://img.shields.io/github/created-at/selfcustody/krux-installer)](https://github.com/selfcustody/krux-installer/commit/5d177795fe3df380c54d424ccfd0f23fc7e62c41)
[![downloads](https://img.shields.io/github/downloads/selfcustody/krux-installer/total)](https://github.com/selfcustody/krux-installer/releases)
[![downloads (latest release)](https://img.shields.io/github/downloads/selfcustody/krux-installer/latest/total)](https://github.com/selfcustody/krux-installer/releases)
[![commits (since latest release)](https://img.shields.io/github/commits-since/selfcustody/krux-installer/latest/main)](https://github.com/qlrd/krux-installer/compare/main...kivy)

Krux Installer is a GUI based tool to flash [Krux](https://github.com/selfcustody/krux)
without typing any command in terminal for [flash the firmware onto the device](https://selfcustody.github.io/krux/getting-started/installing/#flash-the-firmware-onto-the-device).

## System setup

Make sure you have python:

```bash
python --version
```
## Linux

Generally, all Linux come with python.

### MacOS

Before installing `krux-installer` source code, you will need:

1. to install `brew` package manager:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install latest `python`:

```bash
brew install python
```

and add this line to your `~/.zshrc`:

```bash
alias python=python3
```

3. Ensure `openssl`:

Python's `ssl` module relies on OpenSSL for cryptographic operations. Ensure that OpenSSL
is installed on your system and is compatible with the Python version you're using.

Since we expect that you're using the Python installed with Homebrew, it's recommended to
install OpenSSL through Homebrew if it's not already installed:

```bash
brew install openssl
```

After installing OpenSSL, make sure it's linked correctly:

```bash
brew link --force openssl
```

This ensures that the OpenSSL libraries are available in the expected
locations that Python can find and use.

4. Patch your `~/.zshrc` (or equivalent):

Library paths on MacOS involves verifying that the environment variables and system
configurationsare correctyly set to find the necessary libraries, such as OpenSSL,
which is crucial for the `ssl` module in Python.

On MacOS, the dynamic linker tool `dyld` uses environment variabes to locate shared
libraries. The primary environment variable for specifying library paths is `DYLD_LIBRARY_PATH`.

Adding the lines below to your `~/.zshrc` (or similar) the `DYLD_LIBRARY_PATH` will be set
each time you open a new terminal session (and therefore the OpenSSL libraries
`libcrypto.dylib` and `libssl.dylib` will can be found):

```bash
OPENSSL_MAJOR_VERSION=`openssl --version | awk '{ print $2}' | cut -d . -f1`
OPENSSL_FULL_VERSION=`openssl --version | awk ' { print $2}'`
export DYLD_LIBRARY_PATH="/opt/homebrew/Cellar/openssl@$OPENSSL_MAJOR_VERSION/$OPENSSL_FULL_VERSION/lib:$DYLD_LIBRARY_PATH"
```

## Install poetry

Make sure you have `poetry` installed:

```b̀ash
python -m pipx install poetry
````

If you have problems with installation, make sure to
properly [configure its options](https://pipx.pypa.io/latest/installation/#installation-options).

## Installation

Clone the repository
```bash
git clone --recurse-submodules --branch kivy https://github.com/krux-installer.git
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

Krux-Installer uses `poe` task manager for formatting, linting,
tests and coverage. To see all available tasks, run:

```bash
poetry run poe
```

### Format code

```bash
poetry run poe format
```

### Lint

```bash
poetry run poe lint
```

### Test

```
poetry run poe test
```

For systems without a window manager:

```bash
poetry run poe test --no-xvfb
```

### Build

At the moment, you'll need to [patch some code on `kivy`](https://github.com/kivy/kivy/issues/8653#issuecomment-2028509695)
to build the Graphical User Interface:

**Linux**:

```
poetry run poe patch-nix
```

**Windows**:

```
poetry run poe patch-win
```

**MacOS**:


Then install  `python`, and `openssl`
modules with the `brew` package manager:

``
- Install latest python: ``
find the `ssl` library (necessary for make https requests with `requests` module).

Con


To do this, you will need these lines 

```
poetry run poe patch-nix
```

Then you can build `krux-installer` as standalone executable:

```bash
poetry run poe build
```

It will export all project in a binary:

- linux: `./dist/krux-installer`
- macOS: `./dist/krux-installer.app/Contents/MacOS/krux-installer`
- windows: `./dist/krux-installer.exe`
