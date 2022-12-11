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

### Lint

```bash
yarn run lint
```

### Generate icons

```bash
yarn run icon
```

### Compiles to a development electron application

```bash
# This runs on dedicated chrome instance
yarn run serve
```

### Compiles and minifies for production

```bash
yarn run build <target> 
```

The `<target>` depends depends on the running platform (i.e., linux, darwin, win32):

* Linux:   
    * `AppImage`
    * `deb`
    * `snap`

* Windows: 
    * `nsis`
    * `portable`
    * `AppX`

* Mac:
    * `dmg`
    * `pkg`
    * `mas`
