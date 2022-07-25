# Krux Installer

Krux Installer (Work In Progress) aims to be a GUI based tool to build, flash and debug [Krux](https://github.com/selfcustody/krux)
to devices.

As it now, the generated application only runs a "Home" interface with some links.

## Download

```bash
git clone https://github.com/qlrd/krux-installer.git
```

### Install dependencies

```bash
yarn install
```

### Compiles and hot-reloads for development

```bash
# This runs on browser
yarn serve

# This runs on dedicated chrome instance
yarn electron:serve
```

### Compiles and minifies for production

* Linux:   `yarn electron:build --linux`
* Windows: `DISPLAY=:0 yarn electron:build --win`
* Mac:     `yarn electron:build --mac`

### Lints and fixes files

```bash
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### Dockerization

This repository provides a docker image, with the aim to compile in a fresh environment.
At the moment, works only to generate `.AppImage`. For windows, needs an better wine configuration.

* docker
* docker-compose

#### build docker image:

```bash
docker-compose build installer
```

#### Execute instances


* Linux: generates an `Krux Installer v*.AppImage` and a `Krux Installer v*.snap`

```bash
docker-compose run installer --linux
```

* Windows: generates an `Krux Installer v*.exe`

```bash
docker-compose run installer --win
```

* Mac: generates an `Krux Installer v*.dmg`

```bash
docker-compose run installer --mac
```
