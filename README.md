[![Build](https://github.com/qlrd/krux-installer/actions/workflows/build.yml/badge.svg)](https://github.com/qlrd/krux-installer/actions/workflows/build.yml)

# Krux Installer

Krux Installer (alpha versions) aims to be a GUI based tool to build, flash and debug [Krux](https://github.com/selfcustody/krux) Kendryte K210 devices
(m5stickV, Sipeed Amigo, Sipeed Bit and Sipeed Dock).

As it now, the generated application execute, without typing any command in terminal,[flash the firmware onto the device](https://selfcustody.github.io/krux/getting-started/installing/#flash-the-firmware-onto-the-device), for Linux and Windows.

## Download

```bash
git clone https://github.com/qlrd/krux-installer.git
```

### Install dependencies

```bash
yarn install
```

## Develop

### Compiles and hot-reloads for development in browser

```bash
# This runs on browser
yarn run serve
```

### Compiles to a development electron application

#### Linux and MacOS

```bash
# This runs on dedicated chrome instance
yarn run electron:serve
```

#### Windows

```bash
# This runs on dedicated chrome instance
yarn run electron:serve:win
```

### Compiles and minifies for production

* Linux:   `yarn run electron:build --linux <target>`
* Windows: `yarn run electron:build --win <target>`
* Mac:     `yarn run electron:build --mac <target>`

Where target can be:

* Linux: AppImage, deb or snap
* Windows: nsis, msi, portable
* Mac: dmg, pkg

Any generated binary will be placed at `dist_electron` folder.