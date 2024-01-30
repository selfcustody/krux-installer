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

After forma:

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
