# CLAUDE.md

Instructions for Claude Code when working on krux-installer.

## Project overview

A GUI application (Python/Kivy) to flash [Krux](https://github.com/selfcustody/krux)
firmware on K210-based Bitcoin hardware wallet devices.

- **Entry point:** `krux_installer.py`
- **Backend (business logic):** `src/utils/`
- **Frontend (GUI screens):** `src/app/`
- **Unit tests:** `tests/`
- **End-to-end tests:** `e2e/`, `e2e_drives/`
- **i18n:** `src/i18n/` (13 locales, JSON format)
- **Build scripts:** `.ci/`
- **CI/CD:** `.github/workflows/`

## Commands

```sh
# Development
poetry run poe dev          # Run app (info level)
poetry run poe dev-debug    # Run app (debug level)

# Format
poetry run poe format       # Black on all code

# Lint
poetry run poe lint         # jsonlint (i18n) + pylint (src, tests, e2e)

# Test
poetry run poe test-unit    # Unit tests (src/utils, src/i18n)
poetry run poe test-e2e     # E2E tests (src/app screens)
poetry run poe test-drives  # E2E drive tests
poetry run poe test         # All tests

# Build
poetry run poe build-linux
poetry run poe build-macos
poetry run poe build-win
```

## Commit conventions

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `i18n`, `ci`, `chore`

All commits **must** be GPG signed. Atomic commits that individually compile
and pass tests.

## Code style

- **Formatter:** Black (enforces 88-char line length for all code)
- **Linter:** Pylint (max line: 100 as a lenient upper bound for non-Black-managed cases,
  max statements: 50, see `.pylint/src`)
- **Python:** >=3.12.0 required
- **Naming:** `snake_case` (functions, variables), `PascalCase` (classes),
  `UPPER_CASE` (constants)

Every Python file starts with the MIT license header:

```python
# The MIT License (MIT)
# Copyright (c) 2021-2024 Krux contributors
# ...
"""
filename.py

Brief description of what this module does.
"""
```

Classes include a docstring with the class name and description.
Methods include a brief one-line docstring.

## Architecture patterns

- Most utility classes inherit from `Trigger` (`src/utils/trigger/`),
  which provides `.info()`, `.debug()`, `.warning()`, `.error()`, `.critical()`
  logging methods.
- Screen classes inherit from `BaseScreen` (Kivy Screen + Trigger).
- Use `@property` getters/setters with debug logging.
- Prefer explicit error handling over silent `None` returns.

## Device support

Devices are defined in `src/utils/constants/__init__.py`:
- `VALID_DEVICES`: list of device names
- `VALID_DEVICES_VERSIONS`: dict mapping device → `{initial, final}` version range

To add a new device:
1. Add to `VALID_DEVICES` list
2. Add version range to `VALID_DEVICES_VERSIONS`
3. Add VID in `BaseFlasher.DEVICE_VID_MAP` (`src/utils/flasher/base_flasher.py`)
4. Add board in `BaseFlasher.DEVICE_BOARD_MAP`
5. Update `SelectDeviceScreen` grid rows and tests
6. Add unit tests in `tests/test_000_constants.py`
7. Add E2E tests in `e2e/test_004_select_device_screen.py`

## Testing

- **Test runner:** `pytest`; some test classes use `unittest.TestCase`-style structure
- Mocking: `unittest.mock` (`patch`, `MagicMock`)
- E2E: `kivy.tests.common.GraphicUnitTest`
- Shared mocks in `tests/shared_mocks.py`
- Coverage target: 95% for critical parts (`src/utils`), currently ~98% overall
- Test file naming: `test_NNN_module_name.py` (sequential numbering)

## CI checks

All PRs must pass:
1. Conventional Commits validation
2. Black formatting (`--check`)
3. Pylint (separate configs for src and tests)
4. Pytest on Linux (x64), Windows (x64), macOS (arm64)
5. Markdown lint (markdownlint-cli, MD033 disabled)
6. LICENSE file must not be modified
