#!/usr/bin/env bash

set -euo pipefail

# ====== Config ======
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DISTRO="${1:-noble}" # Default to 'noble' if no arg is passed
CHROOT_DIR="/srv/chroot/${DISTRO}-amd64"
CHROOT_NAME="${DISTRO}-amd64-sbuild"
MIRROR="http://archive.ubuntu.com/ubuntu"
ARTIFACTS_DIR="${SCRIPT_DIR}/output/artifacts"
BUILD_DIR="$HOME/sbuild-builds"
PACKAGE_NAME="krux-installer"

# ====== Remove old chroot ======
echo "🚧 Removing existing sbuild chroot for: $DISTRO"
sudo rm -rf "$CHROOT_DIR"
sudo rm -f "/etc/sbuild/chroot/${CHROOT_NAME}"
sudo rm -f "/etc/schroot/chroot.d/${CHROOT_NAME}"*
sudo rm -rf "/var/lib/sbuild/${CHROOT_NAME}"

# ====== Create new chroot ======
echo "🛠️  Creating new sbuild chroot..."
sudo sbuild-createchroot \
  --include=eatmydata \
  --components=main,universe,multiverse,restricted \
  "$DISTRO" "$CHROOT_DIR" "$MIRROR"

# ====== Add current user to sbuild group ======
if ! groups "$USER" | grep -qw sbuild; then
  echo "➕ Adding user $USER to 'sbuild' group"
  sudo sbuild-adduser $USER
  #sudo usermod -aG sbuild "$USER"
  #newgrp sbuild
  echo "⚠️ Please log out and log back in to apply group membership."
fi

# ====== Prepare build files ======
echo "📦 Copying build artifacts from $ARTIFACTS_DIR to: $BUILD_DIR"
mkdir -p "$BUILD_DIR"
cp "$ARTIFACTS_DIR"/${PACKAGE_NAME}_* "$BUILD_DIR"

# ====== Run sbuild ======
echo "🚀 Starting build..."
cd "$BUILD_DIR"
LATEST_DSC=$(ls -1 ${PACKAGE_NAME}_*.dsc | sort | tail -n 1)

sbuild -d "$DISTRO" "$LATEST_DSC"

echo "✅ Build finished."
