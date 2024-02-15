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
git clone --branch kivy https://github.com/krux-installer.git
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

That is similar to:

```bash
poetry run black ./src
poetry run black ./tests
```

### Lint

After format:

```
poetry run poe lint
```

That is simlar to:

```
poetry run pylint ./src
poetry run pylint --disable=C0114,C0115,C0116 ./tests
```

### Test

Krux-Installer uses `poe` task manager for tests:

```bash
poetry run poe test
```

That is simlar to:

```bash
poetry run pytest --capture=tee-sys --verbose --cache-clear ./tests
```

### Coverage

After tests, will be worth to run coverage:

```
poetry run poe coverage-html
```

That is simlar to:

```bash
poetry run pytest --cache-clear --cov src/ --cov-report html ./tests
```

## CLI

At the moment, the script `krux-installer.py` can be executed in a `poetry shell` like a CLI (Command Line Interface).

To do this, you must do:

```
$> poetry shell
```

Once new shell is spwaned, execute `python ./krux-installer` followed by two dashes (`--`) and the command arguments:

```
$> python ./krux-installer.py -- --help                     
[INFO   ] [Logger      ] Record log in /home/user/.kivy/logs/kivy_some_date.txt
[INFO   ] [Kivy        ] v2.3.0
[INFO   ] [Kivy        ] Installed at "/home/user/.cache/pypoetry/virtualenvs/krux-installer-blabla3.11/lib/python3.11/site-packages/kivy/__init__.py"
[INFO   ] [Python      ] v3.11.7 (main, some date, some hour) [GCC some gcc]
[INFO   ] [Python      ] Interpreter at "/home/user/.cache/pypoetry/virtualenvs/krux-installer-blabla-py3.11/bin/python"
[INFO   ] [Logger      ] Purge log fired. Processing...
[INFO   ] [Logger      ] Purge finished!
usage: krux-installer [-h] [-v] [-a] [-A] [-d FIRMWARE_DEVICE] [-f FIRMWARE_VERSION] [-D DESTDIR] [-F]

A GUI based application to flash Krux firmware on K210 based devices

options:
  -h, --help            show this help message and exit
  -v, --version         Show version
  -a, --available-firmwares
                        Show available versions (require internet connection)
  -A, --available-devices
                        Show available devices
  -d FIRMWARE_DEVICE, --firmware-device FIRMWARE_DEVICE
                        Select a device to be flashed
  -f FIRMWARE_VERSION, --firmware-version FIRMWARE_VERSION
                        Select a firmware version to be flashed
  -D DESTDIR, --destdir DESTDIR
                        Directory where assets will be stored (default: OS tmpdir)
  -F, --flash           If set, download the kboot.kfpkg firmware and flash. Otherwise, download firmware.bin and store in destdir
```
