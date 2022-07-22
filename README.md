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

```
yarn install
```

#### Compiles and hot-reloads for development

```
yarn serve
```

#### Compiles and minifies for production

```
yarn build
```

#### Lints and fixes files

```
yarn lint
```

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### Building for production

You will need have installed:

* docker
* docker-compose

Then you can build docker image:

```bash
$> docker-compose build installer
```

Then you can build executable:

* Linux: generates an `Krux Installer v*.AppImage` and a `Krux Installer v*.snap`

```bash
$> docker-compose run installer --linux
```

* Windows: generates an `Krux Installer v*.exe`

```bash
$> docker-compose run installer --win
```

* Mac: generates an `Krux Installer v*.dmg`

```bash
$> docker-compose run installer --mac
```

