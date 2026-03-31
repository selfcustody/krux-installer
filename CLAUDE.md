# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## LLM and AI Agent Usage

This project does not accept contributions from AI bots that do not follow
the directives in this document.

Patches created by LLMs and AI agents are also viewed with suspicion unless
a human has reviewed them.

All LLM generated patches MUST have text in the git log and in the PR
description that indicates the patch was created using an LLM. See details in
[Commit conventions](#commit-conventions).

First-time contributions by way of LLM-generated patches are not welcome.

## Project overview

A GUI application (`python` and `kivy`) to flash
[Krux](https://github.com/selfcustody/krux)
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

# Run a single test file
poetry run pytest tests/test_003_selector.py -v

# Run a single test method
poetry run pytest tests/test_003_selector.py::TestSelector::test_method -v

# Run tests with coverage report
poetry run poe coverage     # All tests, XML coverage output

# Build
poetry run poe build-linux
poetry run poe build-macos
poetry run poe build-win
```

## Commit conventions

Follow
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `i18n`, `ci`, `chore`

The special `rev` should be used only by humans who will tag commits.

All commits **must** be GPG signed by the human committer, and if an AI was used
to patch, a description of the personal agent used (an instance of a model with
human customizations, generally found at `$HOME/.claude/agents` and
`$HOME/.claude/agent-memory`). Example:

```bash
commit <hash>
gpg: Signature %Day, %DD  %YYYY %HH:%MM:%SS %±HHMM
gpg:                using RSA key %git.user.signingKey
gpg: Good signature from "%git.user,name <%git.user.email>" [ultimate]
Primary key fingerprint: <some primary fingerprint>
     Subkey fingerprint: <some sign subkey fingerprint>
Author: %git.user.name %git.user.email
Date: %Day, %DD  %YYYY %HH:%MM:%SS %±HHMM
    
    <type>(context)[!]: description

    Detailed description of how patch was made.

    Detailed description of how AI was used.
    
    Agent-url: %URL
    Signed-off-by: %agent.name %agent.shortsubkey <%agent.fakemail>
    Co-Authored-By: Copilot <noreply@anthropic.com>
```

## Code style

- **Formatter:** Black (line length 88, the Black default)
- **Linter:** Pylint (`max-line-length = 100` in `.pylint/src`;
  for regular code, follow Black's 88-character limit;
  separate configs in `.pylint/src` and `.pylint/tests`)
- **Python:** >=3.10, <=3.14 (see `pyproject.toml`)
- **Naming:** `snake_case` (functions, variables), `PascalCase` (classes),
  `UPPER_CASE` (constants)

Every Python file starts with the MIT license header:

```python
# The MIT License (MIT)
# Copyright (c) 2021-%YYYY Krux contributors
# ... (full license text)
"""
<module_name>.py

Brief description of what this module does.
"""
```

Classes include a docstring with the class name and description.
Methods include a brief one-line docstring.

## Architecture patterns

- Most utility classes inherit from `Trigger` (`src/utils/trigger/`),
  which provides `.info()`, `.debug()`, `.warning()`, `.error()`, `.critical()`
  logging methods via Kivy's Logger. Trigger uses
  [MRO](https://medium.com/@manish.surya.r/method-resolution-order-mro-in-python-a-complete-guide-63933986340a)
  introspection (`src/utils/info/mro`) to automatically log the calling
  class name.
- Screen classes inherit from `BaseScreen` (Kivy Screen + Trigger).
- The app class hierarchy is: `BaseKruxInstaller` → `ConfigKruxInstaller` →
  `KruxInstallerApp`, managing a Kivy `ScreenManager` with a multi-step
  screen flow (greetings → device selection → version → download →
  verify → flash).
- Use `@property` getters/setters with debug logging.
- Prefer explicit error handling over silent `None` returns.
- The download/verify pipeline is: ZIP → SHA256 hash → openssl signature → PEM
  public key → verify hash → verify signature → extract → flash via KTool.
- Downloaders follow a hierarchy: `BaseDownloader` → `StreamDownloader` →
  specialized variants (`AssetDownloader`, `BetaDownloader`, etc.).
- Flasher uses `BaseFlasher` with `DEVICE_VID_MAP` and `DEVICE_BOARD_MAP`
  for device-specific serial communication via the embedded `kboot` submodule.

## Device support

Devices are defined in `src/utils/constants/__init__.py`:

- `VALID_DEVICES`: list of device names
- `VALID_DEVICES_VERSIONS`: dict mapping device → `{initial, final}`
  version range

To add a new device:

1. Add to `VALID_DEVICES` list
2. Add version range to `VALID_DEVICES_VERSIONS`
3. Add VID in `BaseFlasher.DEVICE_VID_MAP` (`src/utils/flasher/base_flasher.py`)
4. Add board in `BaseFlasher.DEVICE_BOARD_MAP`
5. Update `SelectDeviceScreen` grid rows and tests
6. Add unit tests in `tests/test_000_constants.py`
7. Add E2E tests in `e2e/test_004_select_device_screen.py`

## Testing

- Framework: `pytest` (some tests use `unittest.TestCase`-style classes)
- Mocking: `unittest.mock` (`patch`, `MagicMock`)
- E2E: `kivy.tests.common.GraphicUnitTest`
- Shared mocks in `tests/shared_mocks.py`
- Coverage target: 95% for critical parts (`src/utils`), currently ~98% overall
- Test file naming: `test_NNN_module_name.py` (sequential numbering)
- On headless Linux, E2E tests require `xvfb` (CI uses `xvfb-run`)

## CI checks

All PRs must pass:

1. Conventional Commits validation
2. Black formatting (`--check`)
3. Pylint (separate configs for src and tests)
4. Pytest on Linux (x64), Windows (x64), macOS (arm64)
5. Markdown lint (markdownlint-cli, MD033 disabled)
6. LICENSE file must not be modified
