# Krux Installer

[![Build main branch](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml)

[![codecov](https://codecov.io/gh/qlrd/krux-installer/tree/kivy/graph/badge.svg?token=KD41H20MYS)](https://codecov.io/gh/qlrd/krux-installer)

Krux Installer aims to be a GUI based tool to build,
flash and debug [Krux](https://github.com/selfcustody/krux)

As it now, the generated application execute, without typing any
command in terminal the [flash the firmware onto the device](https://selfcustody.github.io/krux/getting-started/installing/#flash-the-firmware-onto-the-device).


## Install

Make sure you have python:

```bash
python --version
```

Make sure you have `poetry` installed:

```b̀ash
python -m pipx install poetry
````

Clone the repository
```bash
git clone --recurse-submodules --branch kivy https://github.com/krux-installer.git
```

* If already cloned the repo without using `--recurse-submodules`, use the command below to clone the needed submodules:
```bash
git submodule update --init
```

Install python dependencies:

```b̀ash
poetry install
```

## Poe the poetry

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

After format:

```
poetry run poe lint
```

### Test

Krux-Installer uses `poe` task manager for tests. This will generate a
`htmlcov/index.html` folder with coverage results to navigate in a browser.

```bash
poetry run poe test
```

## Build

To build `krux-installer` as standalone executable, run:

```bash
poetry run poe build
```

It will export all project in a binary
(without extension for linux and macOS and with `.exe` for windows)
located at `./dist/krux-installer`.


## CLI

Running `./dist/krux-installer --help` (linux and macOS) or `./dist/krux-installer.exe --help` (windows),
you will have this terminal output:

```bash
usage: krux-installer [-h] [-v] [-a] [-A] [-d DEVICE] [-f FIRMWARE] [-D DESTDIR] [-F] [-w] [-s SIGN] [-S] [-V VERIFY] [-K FILENAME] [-p PUBKEY]

A GUI based application to flash Krux firmware on K210 based devices

options:
  -h, --help            show this help message and exit
  -v, --version         Show version
  -a, --available-firmwares
                        Show available versions (require internet connection)
  -A, --available-devices
                        Show available devices
  -d DEVICE, --device DEVICE
                        Select a device to be flashed
  -f FIRMWARE, --firmware FIRMWARE
                        Select a firmware version to be flashed
  -D DESTDIR, --destdir DESTDIR
                        Directory where assets will be stored (default: OS tmpdir)
  -F, --flash           If set, download the kboot.kfpkg firmware and flash. Otherwise, download firmware.bin and store in destdir
  -w, --wipe            Erase all device's data and firmware (CAUTION: this will make the device unable to work until you install a new firmware)
  -s SIGN, --sign SIGN  sign a file with your device
  -S, --save-hash       save a sha256.txt file when signing with your device
  -V VERIFY, --verify VERIFY
                        verify the authenticity of a signature file (.sig) signed with krux
  -K FILENAME, --filename FILENAME
                        the file to be verified with --verify option
  -p PUBKEY, --pubkey PUBKEY
                        the public key certificate (.pem) to be verified with --verify option
```

### Check firmwares with `--available-firmwares`

List which firmware versions are available on github:

```
$> ./dist/krux-installer --available-firmwares
```

### Check devices with `--available-devices`

List which devices are supported:


```
$> ./dist/krux-installer --available-devices
```

### Flash official firmware for some device with `--firmware`, `--device` and `--flash`

```
$> ./dist/krux-installer --firmware v24.03.0 --device amigo --flash
```


### Flash beta firmware for some device with `--firmware`, `--device` and `--flash`

```
$> ./dist/krux-installer --firmware odudex/krux_binaries --device amigo --flash
```

### Only download official firmware binary to do an airgapped update with `--firmware` and `--device`

```
$> ./dist/krux-installer --firmware v24.03.0 --device amigo
```

### Only download beta firmware binary to do an airgapped update with `--firmware` and `--device`

```
$> ./dist/krux-installer --firmware odudex/krux_binaries --device amigo
```


### Wipe (erase firmware for emergencies) for some device with `--device` and `--wipe`

```
$> ./dist/krux-installer --device amigo --wipe
```

### Sign any file with your device with `--sign`

```
$> ./dist/krux-installer --sign myfile.txt
```
  
### Sign any file with your device and save a sha256sum file of iw with `--sign` and `--save-hash`

```
$> ./dist/krux-installer --sign myfile.txt --save-hash
```


### Verify the authenticity of any file signed with krux with `--verify`, `--filename` and `--pubkey`

```
$> ./dist/krux-installer --verify myfile.txt.sig --filename myfile.txt --pubkey myfile.txt.pem
```

## TODO

- add `--gui` option to run an Graphical User Interface with kivy.
