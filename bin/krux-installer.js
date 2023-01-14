const { exec, spawn } = require('child_process');
const { existsSync } = require('fs');
const { platform } = require('os');
const { join } = require('path');
const { name, version, platformDependencies } = require('../package.json')

const action = process.argv[2]
const executable = {}
const env = {}

const delay = 5000
let index = 0

let onClose = null

const promises = []

// Staggered Promises with Promise.all
// SEE https://replit.com/@goforthandrock/Staggered-Promises-with-Promiseall?v=1#index.js
function runner (cmd, args, env) {
  promises.push(new Promise(async function(resolve) {

    await new Promise(function(res) {
      index += 1
      setTimeout(res, delay * index)
    })

    let service
    let bin

    if (cmd !== 'yarn') {
      bin = join(__dirname, '..', 'node_modules', '.bin', cmd)
    }
    if (cmd === `yarn${process.platform === 'win32' ? '.cmd' : '' }`) {
      bin = cmd
    }

    console.log(`  running \x1b[32m${cmd}\x1b[0m \x1b[33m${args.join(' ')}\x1b[0m`);

    if (args.indexOf('<') !== -1 || args.indexOf('>') !== -1) {
      resolve(await new Promise(function(res, rej) {
        exec(`${bin} ${args.join(' ')}`, function (error, stdout, stderr) {
          if (error) rej(error)
          if (stderr) rej(new Error(stderr))
          res(`  finished \x1b[32m${cmd}\x1b[0m \x1b[33m${args.join(' ')}\x1b[0m exit code: 0`);
        })
      }))
    } else {
      resolve(new Promise(function(res, rej) {
        const service = spawn(bin, args, { env: env || process.env });

        const onData = function(data) {
          let msg = data.toString()
          msg = msg.replace(/\n$/, '')
          console.log(msg)
        }
        service.stdout.on('data', onData)
        service.stderr.on('data', onData)

        service.on('close', function(code) {
          res(`  finished \x1b[32m${cmd}\x1b[0m \x1b[33m${args.join(' ')}\x1b[0m exit code: ${code}`);
        });
      }))
    }
  }))
}

async function main() {
  console.log("");
  console.log(`   ${name} ${version}`);
  console.log(" ████████████████████████████████");
  console.log(" ██                            ██");
  console.log(" ██           ██               ██");
  console.log(" ██           ██               ██");
  console.log(" ██           ██               ██");
  console.log(" ██           ██               ██");
  console.log(" ██         ██████             ██");
  console.log(" ██           ██               ██");
  console.log(" ██           ██  ██           ██");
  console.log(" ██           ██ ██            ██");
  console.log(" ██           ████             ██");
  console.log(" ██           ██ ██            ██");
  console.log(" ██           ██  ██           ██");
  console.log(" ██           ██   ██          ██");
  console.log(" ██                            ██");
  console.log(" ████████████████████████████████");
  console.log("");

  if (action === 'lint') {
    runner(`vue-cli-service${process.platform === 'win32' ? '.cmd' : '' }`, ['lint'])
    runner(`eslint${process.platform === 'win32' ? '.cmd' : '' }`, [ join(__dirname, '..', 'public') ])
    runner(`eslint${process.platform === 'win32' ? '.cmd' : '' }`, [ join(__dirname, '..', 'src') ])
    runner(`eslint${process.platform === 'win32' ? '.cmd' : '' }`, [ '--ext', 'ts', join(__dirname, '..', 'test/pageobjects') ])
    runner(`eslint${process.platform === 'win32' ? '.cmd' : '' }`, [ '--ext', 'ts', join(__dirname, '..', 'test/specs') ])
  }

  if (action === 'icon') {
    const fromTxt = join(__dirname, '..', 'build', 'krux.txt')
    const toSvg = join(__dirname, '..', 'build', 'krux.svg')
    runner(`aasvg${process.platform === 'win32' ? '.cmd' : '' }`, ['<', fromTxt, '>', toSvg])

    const toPng = join(__dirname, '..', 'build', 'krux.png')
    runner(`svgexport${process.platform === 'win32' ? '.cmd' : '' }`, [toSvg, toPng])

    const toIconPng = join(__dirname, '..', 'build', 'icon.png')
    runner(`resize-img${process.platform === 'win32' ? '.cmd' : '' }`, ['--width', '256', '--height', '256', toPng, '>', toIconPng])

    if (process.platform === 'win32') {
      const toIcon = join(__dirname, '..', 'build', 'icon.ico')
      const ico = runner('png-to-ico.cmd', [ toIconPng, '>', toIcon ])
      promises.push(ico)
    }

    if (process.platform === 'darwin') {
      const toIcns = join(__dirname, '..', 'build')
      const icns = runner('mk-icns', toIconPng, toIcns)
      promises.push(icns)
    }
  }

  if (action === 'serve') {

    env.DEBUG = 'krux:*'

    if (process.platform === 'win32') {
      env.ProgramFiles = process.env.ProgramFiles
    }

    const cmd = `vue-cli-service${process.platform === 'win32' ? '.cmd' : '' }`
    runner(cmd, [`electron:${action}`], {
      ...env,
      ...process.env
    })
  }

  if (action === 'build') {

    const target = process.argv[3]
    let args = null

    if (process.platform === 'linux') {
      args = [`electron:${action}`, '--linux', target]
    }

    if (process.platform === 'darwin') {
      args = [`electron:${action}`, '--mac', target]
    }

    if (process.platform === 'win32') {
      args = [`electron:${action}`, '--win', target]
    }

    const cmd = `vue-cli-service${process.platform === 'win32' ? '.cmd' : '' }`
    runner(cmd, args)
  }


  if (action === 'platform-install') {
    const dependencies = platformDependencies[process.platform]

    const pkgs = Object.keys(dependencies)
    for (let i in pkgs){
      const name = pkgs[i];
      const version = dependencies[name];
      const module = join(__dirname, '..', 'node_modules', name)
      console.log(`  \x1b[34m\u2022\x1b[0m installing platform dependency ${name} for ${process.platform}`)
      runner(`yarn${process.platform === 'win32' ? '.cmd' : '' }`, ['add', '--dev', `${name}@${version}`])
    }
  }

  if (action === 'install-app-deps') {
    runner(`electron-builder${process.platform === 'win32' ? '.cmd' : '' }`, [action])
  }

  if (action === 'test') {
    const wdioconf = join(__dirname, '..', 'wdio.conf.js')

    if (process.platform === 'linux') {
      runner('xvfb-maybe', ['wdio', 'run', wdioconf ])
    } else {
      runner(`wdio${process.platform === 'win32' ? '.cmd' : '' }`, ['run', wdioconf])
    }
  }

  try {
    const results = await Promise.all(promises)
    results.forEach(function(result) {
      console.log(result)
    })
  } catch (error) {
    console.log(error)
  }
}

main()
