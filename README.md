# Krux Installer

Krux Installer (Work In Progress) aims to be a GUI based tool to build, flash and debug [Krux](https://github.com/selfcustody/krux)
to devices.

As it now, the generated application only runs a "Home" interface with some links.

## Download

```bash
$> git clone https://github.com/qlrd/krux-installer.git
```

## Development

### Project setup

To [avoid install dependencies every time you build a Docker image](https://stackoverflow.com/questions/52673921/how-do-you-cache-yarn-dependencies-for-a-docker-image-build-in-circleci), setup a `cache` dir to yarn:

```bash
mkdir -p .cache/yarn
YARN_CACHE_DIR=.cache/yarn yarn install
```

#### Compiles and hot-reloads for development

```bash
yarn serve
```

#### Compiles and minifies for production

```bash
yarn build
```

#### Lints and fixes files

```bash
yarn lint
```

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### Building for development


* Linux: generates an `Krux Installer v*.AppImage` and a `Krux Installer v*.snap`

```bash
yarn run electron:build --linux
```

* Windows: generates an `Krux Installer v*.exe`

You will need a `wine` package installed on your system. Once installed, you will run:

```bash
DISPLAY=:0 yarn run electron:build --win
```

* Mac: generates an `Krux Installer v*.dmg`

```bash
yarn run electron:build --mac
```


### Building for production

You will need have installed:

* docker
* docker-compose

Then you can build docker image:

```bash
docker-compose build installer
```

Then you can build executable:

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

