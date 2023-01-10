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

#### Builtin OpenSSL for windows in KruxInstaller

When downloading official krux firmware versions, it is necessary to verify the signature through the OpenSSL tool, as a way to verify the authenticity of the downloaded binaries.

On linux release, verification is easily done since such tool exists natively in operating system.

In windows releasewe are faced with the peculiarity of the operating system in question not having such a tool (see this [issue](https://github.com/qlrd/krux-installer/issues/2)).

So, we packaged a stable version of OpenSSL, compiled from the [source](https://github.com/openssl/openssl). The compilation process is done entirely in a reproducible virtual environment and, therefore, not locally, with the github-action [compile-openssl-windows-action](https://github.com/qlrd/compile-openssl-windows-action/actions).

Since it is compiled in a virtual environment on github, it is expected to be fully verifiable and free of malicious code. You can check the build steps in [actions](https://github.com/qlrd/krux-installer/actions).
