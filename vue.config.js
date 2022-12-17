const { defineConfig } = require('@vue/cli-service')
const path = require('path')
const replace = require('replace')
const fs = require('fs')
const pkg = require('./package.json')

module.exports = defineConfig({
  configureWebpack: {
    devtool: "source-map",
  },
  transpileDependencies: true,
  pluginOptions: {
    electronBuilder: {
      builderOptions: {
        //version: pkg.devDependencies["electron-builder"].split("^")[1],
        appId: "selfcustody.installer.krux",
        productName: "KruxInstaller",
        copyright: "MIT License",
        electronVersion: pkg.devDependencies.electron,
        linux: {
          icon: 'icon.png',
          maintainer: pkg.author
        },
        win: {
          icon: 'icon.ico'
        },
        mac: {
          icon: 'icon.icns'
        },
        files: [
          '!**/{README.md,.github,.browserslistrc,.eslintrc.js,vue.config.js,jsconfig.js,babel.config.js,yarn.lock}',
          '!./bin/{electron-serve.js}'
        ],
        // See
        // 'Can't load fonts in production build, vue-cli@5.0.0-alpha.6'
        // https://github.com/nklayman/vue-cli-plugin-electron-builder/issues/1286
        beforeBuild: function (context) {
          const workDir = path.join(context.appDir, "css")
          const files = fs.readdirSync(workDir);
            replace({
              regex: "app:///fonts",
              replacement: "app://./fonts",
              paths: files.map(val => path.join(workDir, val)),
              recursive: false,
              silent: false,
          })

          return true
        }
      }
    }
  }
})
