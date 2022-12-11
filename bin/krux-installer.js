const { spawn } = require('child_process');
const { platform } = require('os');
const { join } = require('path');

const action = process.argv[2]
const executable = {}
const env = {}

let onClose = null

if (action === 'serve' || action === 'build') {

  if (process.platform === 'linux') {
    executable.cmd = join(__dirname, '..', 'node_modules', '.bin', 'vue-cli-service')
  }

  if (process.platform === 'darwin' && action === 'serve') {
    executable.cmd = join(__dirname, '..', 'node_modules', '.bin', 'vue-cli-service')
  }
  
  if (process.platform === 'win32') {
    executable.cmd = join(__dirname, '..', 'node_modules', '.bin', 'vue-cli-service.cmd')
  }

  executable.args = [`electron:${action}`]; 
}

if (action === 'serve') {

  if (process.platform === 'linux') {
    env.DEBUG = 'krux:*';
  }

  if (process.platform === 'darwin' && action === 'serve') {
    env.DEBUG = 'krux:*'
  }
  
  if (process.platform === 'win32') {
    env.DEBUG = 'krux:*'
    env.ProgramFiles = process.env.ProgramFiles
  }
}

if (action === 'postinstall') {
  const dependencies = {
    'darwin': [
      'dmg-builder@24.0.0-alpha.3',
      'dmg-license@1.011'
    ]
  };

  if (dependencies[platform]) {
    console.log(`  \x1b[34m\u2022\x1b[0m installing dependent platform dependencies for ${platform}`)
    executable.cmd = 'yarn'
    executable.args = ['add', dependencies[platform].join(' ')]
  } else {
    console.log(`  \x1b[34m\u2022\x1b[0m skipping dependent platform dependencies for ${platform}`)
  }
}

if (action === 'install-app-deps') {
  executable.cmd = join(__dirname, '..', 'node_modules', '.bin', 'electron-builder')
  executable.args = action
}

if (executable.cmd) {
  const service = spawn(executable.cmd, executable.args, { env: env });

  service.stdout.on('data', function(data) {
    const message = data.toString();
    console.log(message);
  });

  service.stderr.on('data', function(data) {
    const message = data.toString();
    console.log(message);
  });

  service.on('close', function(code) {
    console.log(`${executable.cmd} ${executable.args.join(' ')} exit code: ${code}`);
  });
}