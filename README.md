[![Build new-ui branch](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml/badge.svg?branch=new-ui)](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml)

# Krux Installer

Krux Installer (alpha versions) aims to be a GUI based tool to build, flash and debug [Krux](https://github.com/selfcustody/krux)

As it now, the generated application execute, without typing any command in terminal,[flash the firmware onto the device](https://selfcustody.github.io/krux/getting-started/installing/#flash-the-firmware-onto-the-device), for Linux and Windows.

## TODOs

- Kendryte K210 devices:
  - [x] Flash to M5stickV;
  - [x] Flash to Sipeed Amigo;
  - [x] Flash to Sipeed Bit;
  - [x] Flash to Sipeed Dock;
  - [ ] Build from source to M5stickV;
  - [ ] Build from source to Sipeed Amigo;
  - [ ] Build from source to Sipeed Bit;
  - [ ] Build from source to Sipeed Dock;
  - [ ] Debug for M5stickV;
  - [ ] Debug for Sipeed Amigo;
  - [ ] Debug for Sipeed Bit;
  - [ ] Debug for Sipeed Dock;
- [odudex Android version](https://github.com/odudex/krux_binaries/tree/main/Android):
  - [ ] Transfer to device;
  - [ ] Build for device;
  - [ ] Debug for device.
- Windows:
  - [x] Build NSIS installer;
  - [ ] Build Portable installer;
  - [ ] Build AppX installer;
- Linux:
  - [x] Build `AppImage` standalone;
  - [ ] Build `deb` package for [apt-get](https://www.debian.org/doc/manuals/apt-howto/);
  - [ ] Build `snap` package for [snapcraft](https://snapcraft.io/);
  - [ ] Build `pacman` package for [pacman](https://wiki.archlinux.org/title/Pacman).
- MacOS:
  - [x] Build DMG installer;
  - [ ] Build PKG installer;
  - [ ] Build MAS installer;

## Install

You can download compiled binaries on [releases page](https://github.com/selfcustody/krux-installer/releases) or Build from source:

## Build from source

### Download

```bash
git clone https://github.com/qlrd/krux-installer.git
```

### Install dependencies

```bash
yarn install
```

### Develop

When a change is made, we recommend to `lint`, `dev`, `build` and `test` procedures before make a commit or a PR:

#### Lint

Verify code style and syntax errors:

```bash
yarn lint
```

#### Compiles to a development electron application
 
Run electron application with the (vite)[https://vitejs.dev/] server:

```bash
yarn dev
```

### Compiles and minifies for production

Before running build, verify [builder config](electron-builder.json5) to setup the build targets. The `<target>` depends depends on the running platform (i.e., linux, darwin, win32):

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


Then run:

```bash
yarn build <target> 
```

#### Builtin OpenSSL for windows in KruxInstaller

When downloading official krux firmware versions, it is necessary to verify the signature through the OpenSSL tool, as a way to verify the authenticity of the downloaded binaries.

On Unix like releases (Linux and MacOS), verification is easily done since such tool exists natively in operating system.

In windows release, we are faced with the peculiarity of the operating system in question not having such a tool (see this [issue](https://github.com/qlrd/krux-installer/issues/2)).

So, we packaged a stable version of OpenSSL, compiled from the [source](https://github.com/openssl/openssl). The compilation process is done entirely in a reproducible virtual environment and, therefore, not locally, with the github-action [compile-openssl-windows-action](https://github.com/qlrd/compile-openssl-windows-action/actions).

Since it is compiled in a virtual environment on github, it is expected to be fully verifiable and free of malicious code. You can check the build steps in [actions](https://github.com/qlrd/krux-installer/actions).
