# Krux Installer

[![Build main branch](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/selfcustody/krux-installer/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/qlrd/krux-installer/graph/badge.svg?token=KD41H20MYS)](https://codecov.io/gh/qlrd/krux-installer)

Krux Installer (alpha versions) aims to be a GUI based tool to build,
flash and debug [Krux](https://github.com/selfcustody/krux)

As it now, the generated application execute,
without typing any command in terminal.

For more information, see [flash the firmware onto the device](https://selfcustody.github.io/krux/getting-started/installing/#flash-the-firmware-onto-the-device).

## Tested machines

- Linux:
  - Archlinux;
  - Ubuntu;
- Windows:
  - Windows 10

## Untested machines

- MacOS

## Install

- See [releases page](https://github.com/selfcustody/krux-installer/releases);
or

- [Build from source](/#build-from-source)

## Build from source

### Download nodejs

First of all, you will need [Node.js](https://nodejs.org)
installed in you system. We recommend use the latest LTS version.

#### Download from Node.js binaries

You can install node.js in your system downloading it from official
[nodejs website](https://nodejs.org/en/download) and following
provided instructions.

#### Download from NVM (Node Version Manager)

Alternatively, if you have a linux or macos system,
you can have multiple versions of Node.js using [nvm](https://github.com/nvm-sh/nvm).

To install nvm,
follow the [instructions](https://github.com/nvm-sh/nvm#installing-and-updating).

Once installed,
we recomend to install the latest LTS node:

```bash
nvm install --lts
```

### Download repository

Now you can download the source code:

```bash
git clone https://github.com/qlrd/krux-installer.git
```

### Install dependencies

Install all dependencies:

```bash
yarn install
```

Additionaly, you can upgrade dependencies to its latest versions.
Have some caution with this command, once that executing this command
can broke some functionalities, mainly those related to the use of
`google-chrome` and `chromiumdriver` in E2e tests.

**TIP**: Before execute this command, always check the latest supported
`chromium` version at
[Electron Stable Releases page](https://releases.electronjs.org/releases/stable)

```bash
yarn upgrade-interactive --latest
```

### Live compile to development environment

When a change is made, we recommend to execute `dev` subcommand:

```bash
yarn run dev
```

if you want to show some debug messages:

```bash
DEBUG=krux:* yarn run dev
```

#### Debug development app with VSCode/VSCodium

If you're codding with VSCode/VSCodium, go to `Run and Debug`
tab and select `Debug App`:

![VScodium Debug](images/vscodium_debug.png)

### Test

#### Prepare tests

To test,
you need to write `specification` tests under `pageobjects` definitions:

- You can write your own [E2E](https://webdriver.io)
specification test files on `test/e2e/specs` folder;

- You can define the [PageObjects] on
`test/e2e/pageobjects` folder.

Before run tests,
you will need to **build** the application.

#### Build

Before running build,
verify [builder config](electron-builder.json5)
to setup the build `target` on specific `os` (Operational System).

The `<target>` depends depends on the running platform
(i.e., `linux`, `darwin` -- MacOS, and `win32` -- Windows).

For more information,
see [Electron Builder](https://www.electron.build/configuration/configuration)
page.

#### Run all tests

The `wdio.conf.mts` is configured to check
if your system have `krux.zip.*` resources.

- If not, it will, run all tests, including download tests;
- If yes, it will skip tests that download resources.

```bash
yarn run build
```

If you want to build a specific `target`
to a specifi `os`, run

```bash
yarn run build --<os> <target>
```

If you want to debug some messages, add the
`DEBUG` environment variable.

In linux/mac:

```bash
DEBUG=krux:* yarn run build --<os> <target>
```

##### Run tests

To run all tests in command line:

```bash
NODE_ENV=test yarn run e2e
```

#### Debug test in VSCode/VSCodium

If you're codding with VSCode/VSCodium, the `NODE_ENV`
variable is already configured. To run, tests, go to `Run and Debug`
tab and select `Test E2E App`:

![VScodium E2E test](images/vscodium.png)
