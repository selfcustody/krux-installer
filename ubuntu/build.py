#!/usr/bin/env python3

"""
Krux Installer CI/CD Build & Packaging Script

Handles:
- Clean source tree
- Export Poetry dependencies (prod + dev)
- Vendor dependencies (incl. dev + poetry)
- Vendor pinned Git-based dependency (pysudoer)
- Generate Debian packaging files (metadata, postinst)
- Patch Kivy PyInstaller hook offline
- Build source tarball and Debian source package
- Log progress to build.log
"""

import argparse
import re
import shutil
import subprocess
import tarfile
import textwrap
from datetime import datetime
from pathlib import Path

LOG_FILE = "build.log"
ZIP_NAME = "pysudoer-0.0.1.zip"
PYSUDOER_REPO = "https://github.com/qlrd/pysudoer.git"
PYSUDOER_COMMIT = "47093f5eef1185e4e652c0ff7324678b01e3b677"
ENTRY_SCRIPT = "krux-installer.py"
MODULE_NAME = "krux_installer"
COPYRIGHT_HEADER = """Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: krux-installer
Source: https://github.com/selfcustody/krux-installer
"""


def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")


def run(cmd, **kwargs):
    log(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kwargs)


def vendor_git_zip(build_dir, zip_path):
    log(f"📦 Vendoring {ZIP_NAME} from Git")
    tmp = build_dir / "tmp_pysudoer"
    run(["git", "clone", PYSUDOER_REPO, str(tmp)])
    run(["git", "checkout", PYSUDOER_COMMIT], cwd=tmp)
    shutil.make_archive(zip_path.with_suffix(""), "zip", root_dir=tmp, base_dir=".")
    shutil.rmtree(tmp)


def export_and_vendor_dependencies(build_dir):
    vendor = build_dir / "vendor"
    vendor.mkdir(parents=True, exist_ok=True)

    req = build_dir / "requirements.txt"
    dev_req = build_dir / "dev-requirements.txt"

    log("Exporting requirements.txt and dev-requirements.txt using Poetry")
    run(["poetry", "export", "--without-hashes", "--output", str(req)], cwd=build_dir)
    run(
        [
            "poetry",
            "export",
            "--with",
            "dev",
            "--without-hashes",
            "--output",
            str(dev_req),
        ],
        cwd=build_dir,
    )

    log("Vendoring pysudoer")
    zip_path = vendor / ZIP_NAME
    vendor_git_zip(build_dir, zip_path)

    for file in [req, dev_req]:
        log(f"Downloading dependencies from {file.name}")
        content = file.read_text()
        content = re.sub(r"^pysudoer\s*@.*", "", content, flags=re.MULTILINE)
        content = re.sub(
            r"^filelock.*$", "filelock>=3.12.2", content, flags=re.MULTILINE
        )
        file.write_text(content)
        for line in content.splitlines():
            if line.strip():
                try:
                    run(["pip", "download", line.strip(), "--dest", str(vendor)])
                except subprocess.CalledProcessError:
                    log(f"⚠️ Failed to download: {line.strip()}")

    log("Vendoring Poetry itself")
    try:
        run(["pip", "download", "poetry", "--dest", str(vendor)])
    except subprocess.CalledProcessError:
        log("⚠️ Failed to download Poetry")


def parse_changelog(changelog_path, version):
    content = changelog_path.read_text()
    pattern = re.compile(
        r"## (?P<version>[^\s]+).*?\n\n(?P<body>.*?)(?=\n## |\Z)", re.DOTALL
    )
    for match in pattern.finditer(content):
        if match.group("version") == version:
            date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
            body = "\n".join(
                f"  * {line.strip('- ')}"
                for line in match.group("body").splitlines()
                if line.strip()
            )
            return date, body
    raise ValueError(f"Version {version} not found in changelog")


def generate_changelog(changelog_path, version, output_path, name, email):
    date, body_raw = parse_changelog(changelog_path, version)
    body = "\n".join(
        textwrap.fill(
            f"  * {line.strip('*- ')}",  # <- only a single leading bullet
            width=79,
            subsequent_indent="    ",
        )
        for line in body_raw.splitlines()
        if line.strip()
    )
    content = f"""krux-installer ({version}-1) unstable; urgency=medium

  {body}

 -- {name} <{email}>  {date}\n"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)


def generate_copyright(license_path, output_path):
    license_text = license_path.read_text()
    content = f"{COPYRIGHT_HEADER}\nFiles: *\nCopyright: {datetime.now().year} SelfCustody\nLicense: {license_text}"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)


def generate_include_binaries(output_dir):
    path = output_dir / "source" / "include-binaries"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "krux-installer-*/assets/*.ttf",
                "krux-installer-*/assets/*.png",
                "krux-installer-*/assets/*.gif",
                "krux-installer-*/assets/*.ico",
                "krux-installer-*/assets/*.icns",
                "krux-installer-*/assets/*.bmp",
            ]
        )
    )


def generate_postinst(output_dir):
    path = output_dir / "debian" / "postinst"
    postinst_content = """#!/bin/sh
set -e

if [ -n "$SUDO_USER" ] && [ "$SUDO_USER" != "root" ]; then
  echo "Adding user $SUDO_USER to 'dialout' group to enable flash procedure..."
  echo "You'll need to reboot your system to enable changes"
  usermod -a -G dialout $SUDO_USER
elif [ -n "$USER" ] && [ "$USER" != "root" ]; then
  echo "Adding user $USER to 'dialout' group to enable flash procedure..."
  echo "You'll need to reboot your system to enable changes"
  usermod -a -G dialout $USER
fi

#DEBHELPER#

exit 0
"""
    path.write_text(postinst_content, encoding="utf-8", newline="\n")
    path.chmod(0o755)


def generate_desktop_file(output_dir):
    path = output_dir / "krux-installer.desktop"
    output_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """[Desktop Entry]
Name=Krux Installer
Comment=Flash Krux firmware to K210 devices
Exec=krux-installer
Icon=utilities-terminal
Terminal=true
Type=Application
Categories=Utility;
StartupNotify=false
"""
    )


def fix_poetry_structure(build_dir):
    src = build_dir / ENTRY_SCRIPT
    dst = build_dir / MODULE_NAME / "__init__.py"
    if src.exists():
        dst.parent.mkdir(exist_ok=True)
        shutil.move(str(src), str(dst))


def copy_to_output(build_dir, output_dir):
    include = [
        ".ci/***",
        "assets/***",
        "img/***",
        "src/***",
        "vendor/***",
        "requirements.txt",
        "dev-requirements.txt",
        "debian/***",
        "ubuntu/***",
        "CHANGELOG.md",
        "LICENSE",
        "README.md",
        "TODO.md",
        "krux-installer.py",
        "poetry.lock",
        "pyproject.toml",
    ]
    run(
        [
            "rsync",
            "-av",
            *[f"--include={i}" for i in include],
            "--exclude=*",
            f"{build_dir}/",
            f"{output_dir}/",
        ]
    )


def build_tarball(output_dir, version):
    tarball = output_dir.parent / f"krux-installer_{version}.orig.tar.gz"
    if tarball.exists():
        tarball.unlink()
    with tarfile.open(tarball, "w:gz") as tar:
        for f in output_dir.rglob("*"):
            arcname = f"krux-installer-{version}/" + str(f.relative_to(output_dir))
            tar.add(f, arcname=arcname)


def clean_source(build_dir):
    run(
        [
            "find",
            str(build_dir),
            "-type",
            "f",
            "(",
            "!",
            "-name",
            "*.png",
            "-a",
            "!",
            "-name",
            "*.gif",
            "-a",
            "!",
            "-name",
            "*.ico",
            "-a",
            "!",
            "-name",
            "*.icns",
            "-a",
            "!",
            "-name",
            "*.bmp",
            "-a",
            "!",
            "-name",
            "*.ttf",
            "-a",
            "!",
            "-path",
            "*/debian/*",
            ")",
            "-exec",
            "dos2unix",
            "{}",
            ";",
        ]
    )
    run(
        [
            "find",
            str(build_dir),
            "(",
            "-name",
            "*.sh",
            "-o",
            "-name",
            "*.py",
            ")",
            "-exec",
            "chmod",
            "+x",
            "{}",
            ";",
        ]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--software-version", required=True)
    parser.add_argument("--changelog", default="CHANGELOG.md")
    parser.add_argument("--license", default="LICENSE")
    parser.add_argument("--maintainer-name", required=True)
    parser.add_argument("--maintainer-email", required=True)
    parser.add_argument("--skip-vendor", action="store_true")
    args = parser.parse_args()

    build_dir = Path(args.build_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    open(LOG_FILE, "w").close()

    clean_source(build_dir)
    if not args.skip_vendor:
        export_and_vendor_dependencies(build_dir)

    copy_to_output(build_dir, output_dir)
    generate_changelog(
        build_dir / args.changelog,
        args.software_version,
        output_dir / "debian" / "changelog",
        args.maintainer_name,
        args.maintainer_email,
    )
    generate_copyright(build_dir / args.license, output_dir / "debian" / "copyright")
    generate_include_binaries(output_dir / "debian")
    generate_postinst(output_dir)
    fix_poetry_structure(build_dir)
    generate_desktop_file(output_dir / "debian" / "usr" / "share" / "applications")
    build_tarball(output_dir, args.software_version)

    run(["dpkg-buildpackage", "-S", "-us", "-uc"], cwd=output_dir)

    artifacts = output_dir / "artifacts"
    artifacts.mkdir(exist_ok=True)
    for ext in (".dsc", ".changes", ".buildinfo", ".debian.tar.xz", ".tar.gz"):
        for f in output_dir.parent.glob(f"*{ext}"):
            shutil.move(str(f), artifacts / f.name)

    log("Build successful. Artifacts:")
    run(["ls", "-lh", str(artifacts)])


if __name__ == "__main__":
    main()
