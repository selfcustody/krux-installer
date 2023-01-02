const { defineConfig } = require('@vue/cli-service');
const path = require('path');
const replace = require('replace');
const fs = require('fs');
const pkg = require('./package.json');

const files = []
files.push('!README.md');
files.push('!.github');
files.push('!.browserslistrc');
files.push('!.eslintrc.js');
files.push('!vue.config.js');
files.push('!jsconfig.js');
files.push('!babel.config.js');
files.push('!yarn.lock');
files.push('!bin/krux-installer.js');
files.push('!build/krux.txt');

if (process.platform === 'linux') {
  files.push('!build/*.ico');
  files.push('!build/*.icns');
}
if (process.platform === 'darwin') {
  files.push('!build/*.png');
  files.push('!build/*.svg');
  files.push('!build/*.ico');
}
if (process.platform === 'win32') {
  files.push('!build/*.png');
  files.push('!build/*.svg');
  files.push('!vendor/OpenSSL/html/*');
  files.push('vendor/OpenSSL/bin/openssl.exe');
  files.push('vendor/OpenSSL/include/*');
  files.push('vendor/OpenSSL/lib/*');
  files.push('vendor/OpenSSL/CommonFiles/*');
}

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
        files: files,
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
});
