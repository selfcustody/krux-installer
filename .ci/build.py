# The MIT License (MIT)

# Copyright (c) 2021-2026 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
.ci/build.py

Runs PyInstaller as a subprocess, captures all output, routes each line
to the appropriate log file under logs/, and keeps the terminal clean.

Terminal output:
  - Default (WARN): spinner — only real fatal errors shown inline
  - --loglevel=TRACE or DEBUG: every line printed, no spinner

Disk output (logs/ directory, one JSON-lines file per level):
  - logs/trace.log  — everything
  - logs/debug.log  — DEBUG and above
  - logs/info.log   — INFO and above
  - logs/warn.log   — WARN and above
  - logs/error.log  — ERROR and CRITICAL only

Usage:
    python .ci/build.py                    # silent terminal, logs/ on disk
    python .ci/build.py --loglevel=INFO    # INFO+ in terminal + logs/
    python .ci/build.py --loglevel=DEBUG   # DEBUG+ in terminal + logs/
    python .ci/build.py --loglevel=TRACE   # everything in terminal + logs/
"""

import argparse
import json
import os
import platform
import re
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent.absolute()
LOGS_DIR = ROOT / "logs"
SPEC_FILE = "krux-installer.spec"

_LEVEL_PRIORITY = {
    "TRACE": 0,
    "DEBUG": 10,
    "INFO": 20,
    "WARN": 30,
    "WARNING": 30,
    "DEPRECATION": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}

_LOG_FILES = [
    ("trace", 0),
    ("debug", 10),
    ("info", 20),
    ("warn", 30),
    ("error", 40),
]

_TERMINAL_LEVELS = {"ERROR", "CRITICAL"}

_VALID_LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"}
_VERBOSE_LEVELS = {"TRACE", "DEBUG"}

_NOISE_PATTERNS = [
    re.compile(r"Spelling.*Unable to find any valuable Spelling provider", re.IGNORECASE),
    re.compile(r"enchant.*ModuleNotFoundError", re.IGNORECASE),
    re.compile(r"osxappkit.*ModuleNotFoundError", re.IGNORECASE),
    re.compile(r"DEPRECATION.*Onefile mode.*macOS", re.IGNORECASE),
    re.compile(r"Library libmtdev", re.IGNORECASE),
    re.compile(r"Library setupapi", re.IGNORECASE),
    re.compile(r"Library Cfgmgr32", re.IGNORECASE),
    re.compile(r"Library Advapi32", re.IGNORECASE),
    re.compile(r"Ignoring.*IOKit.*only basenames are supported", re.IGNORECASE),
    re.compile(r"Ignoring.*CoreFoundation.*only basenames are supported", re.IGNORECASE),
    re.compile(r"Could not find GStreamer", re.IGNORECASE),
]

_PATTERN = re.compile(
    r"^\s*(?:\d+\s+)?"
    r"(TRACE|DEBUG|INFO|WARN|WARNING|DEPRECATION|ERROR|CRITICAL|FATAL)"
    r"[\s:\]]+",
    re.IGNORECASE,
)

if platform.system() == "Windows":
    _SPINNER_FRAMES = ["-", "\\", "|", "/"]
    _CHECK = "[OK]"
    _CROSS = "[FAILED]"
else:
    _SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    _CHECK = "✓"
    _CROSS = "✗"

class Spinner:
    def __init__(self, message: str = "Building krux-installer"):
        self._message = message
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self, success: bool = True):
        self._stop_event.set()
        self._thread.join()
        sys.stdout.write("\r" + " " * (len(self._message) + 4) + "\r")
        sys.stdout.flush()
        if success:
            print(f"{_CHECK} Build complete.")
        else:
            print(f"{_CROSS} Build failed.", file=sys.stderr)

    def _spin(self):
        idx = 0
        while not self._stop_event.is_set():
            frame = _SPINNER_FRAMES[idx % len(_SPINNER_FRAMES)]
            sys.stdout.write(f"\r{frame} {self._message}...")
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1

def _parse_args() -> str:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--loglevel",
        default=os.environ.get("BUILD_LOGLEVEL", "WARN"),
        choices=list(_VALID_LEVELS),
        type=str.upper,
    )
    args, _ = parser.parse_known_args()
    return args.loglevel


def _detect_level(line: str) -> str:
    m = _PATTERN.match(line)
    if m:
        lvl = m.group(1).upper()
        if lvl == "FATAL":
            return "CRITICAL"
        if lvl == "WARNING":
            return "WARN"
        return lvl
    return "INFO"


def _is_noise(line: str) -> bool:
    return any(p.search(line) for p in _NOISE_PATTERNS)


def _make_json_entry(level: str, message: str) -> str:
    return json.dumps(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": message.rstrip(),
        },
        ensure_ascii=False,
    )


def _open_log_files(logs_dir: Path) -> dict:
    logs_dir.mkdir(parents=True, exist_ok=True)
    handles = {}
    for name, priority in _LOG_FILES:
        handles[priority] = open(logs_dir / f"{name}.log", "a", encoding="utf-8")
    return handles


def _write_to_logs(handles: dict, level: str, line: str) -> None:
    line_priority = _LEVEL_PRIORITY.get(level, 20)
    entry = _make_json_entry(level, line)
    for file_priority, fh in handles.items():
        if line_priority >= file_priority:
            fh.write(entry + "\n")
            fh.flush()


def _close_log_files(handles: dict) -> None:
    for fh in handles.values():
        fh.close()

if __name__ == "__main__":
    build_loglevel = _parse_args()
    verbose = build_loglevel in _VERBOSE_LEVELS

    handles = _open_log_files(LOGS_DIR)

    spinner = None
    if not verbose:
        spinner = Spinner()
        spinner.start()
    else:
        print(f"[build] Starting PyInstaller — log level: {build_loglevel}")

    process = subprocess.Popen(
        [sys.executable, "-m", "PyInstaller", SPEC_FILE],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "KIVY_NO_CONSOLELOG": "1"},
    )

    try:
        for raw_line in process.stdout:
            line = raw_line.rstrip()
            if not line:
                continue

            level = _detect_level(line)
            noise = _is_noise(line)

            _write_to_logs(handles, level, line)

            if verbose:
                print(line)
            elif level in _TERMINAL_LEVELS and not noise:
                if spinner:
                    sys.stdout.write("\r" + " " * 60 + "\r")
                    sys.stdout.flush()
                print(line, file=sys.stderr)

    finally:
        process.wait()
        _close_log_files(handles)

    success = process.returncode == 0

    if spinner:
        spinner.stop(success=success)

    if not success:
        print(
            f"Check {LOGS_DIR.relative_to(ROOT)}/error.log for details.",
            file=sys.stderr,
        )

    sys.exit(process.returncode)