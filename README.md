:# Krux Installer

[![Build main branch](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml) [![codecov](https://codecov.io/gh/qlrd/krux-installer/tree/kivy/graph/badge.svg?token=KD41H20MYS)](https://codecov.io/gh/qlrd/krux-installer)

Krux Installer is a GUI based tool to flash [Krux](https://github.com/selfcustody/krux)
without typing any command in terminal for [flash the firmware onto the device](https://selfcustody.github.io/krux/getting-started/installing/#flash-the-firmware-onto-the-device).

## System setup

Make sure you have python:

```bash
python --version
```

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

**Linux and macOS**:

```
poetry run poe patch-nix
```

**Windows**:

```
poetry run poe patch-win
```


Then you can build `krux-installer` as standalone executable:

```bash
poetry run poe build
```

It will export all project in a binary:

- linux and macOS: `./dist/krux-installer`
- windows: `dist/krux-installer.exe`
