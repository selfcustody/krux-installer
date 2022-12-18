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

If you´re developing for Windows or MacOs, run:

```bash
yarn run platform-install
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

#### Openssl for windows

If a user is installing this software for Windows OS, it must have installed a openssl. It be achieved with:

* [Git-SCM GUI](https://git-scm.com/download/win) (RECOMENDED FOR DEVELOPERS);
* [OpenSSL for windows](https://wiki.openssl.org/index.php/Binaries);

If openssl isn´t installed, a message will appear requestig that user install before proceed.

##### OpenSSL Git-SCM GUI

Git-SCM provides a complete solution for developers. If you think that you will be develop for `krux` or `krux-installer`, this is the ideal solution.

##### OpenSSL for Windows

If you do not think develop, the OpenSSL v3.0.7 Light will be enough.

Tested versions:

* [`Shining Light Productions Win64 OpenSSL v3.0.7`](https://slproweb.com/products/Win32OpenSSL.html): Win64 OpenSSL v3.0.7 Light
