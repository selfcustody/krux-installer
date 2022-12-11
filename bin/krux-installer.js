const { exec, spawn } = require('child_process');
const { platform } = require('os');
const { join } = require('path');

const action = process.argv[2]
const executable = {}
const env = {}

const delay = 500
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
    const bin = join(__dirname, '..', 'node_modules', '.bin', cmd)
    console.log(`  \x1b[32m${cmd}\x1b[0m \x1b[33m${args.join(' ')}\x1b[0m`);

    if (args.indexOf('<') !== -1 || args.indexOf('>') !== -1) {
      resolve(await new Promise(function(res, rej) {
        exec(`${bin} ${args.join(' ')}`, function (error, stdout, stderr) {
          if (error) rej(error)
          if (stderr) rej(new Error(stderr))
          res(`  \x1b[32m${cmd}\x1b[0m \x1b[33m${args.join(' ')}\x1b[0m exit code: 0`);
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
          res(`  \x1b[32m${cmd}\x1b[0m \x1b[33m${args.join(' ')}\x1b[0m exit code: ${code}`);
        });
      }))
    }
  }))
}

async function main() {

  if (action === 'lint') {
    runner('vue-cli-service', ['lint'])
    runner('eslint', [ join(__dirname, '..', 'public') ])
    runner('eslint', [ join(__dirname, '..', 'src') ])
  }

  if (action === 'icon') {


    const fromTxt = join(__dirname, '..', 'build', 'krux.txt')
    const toSvg = join(__dirname, '..', 'build', 'krux.svg')
    runner('aasvg', ['<', fromTxt, '>', toSvg])

    const toPng = join(__dirname, '..', 'build', 'krux.png')
    runner('svgexport', [toSvg, toPng])

    const toIconPng = join(__dirname, '..', 'build', 'icon.png')
    runner('resize-img', ['--width', '256', '--height', '256', toPng, '>', toIconPng])

    /*
    if (process.platform === 'win32') {
      const toIcon = join(__dirname, '..', 'build', 'icon.ico')
      const ico = runner('png-to-ico', [ toIconPng, toIcon ])
      promises.push(ico)
    }

    if (process.platform === 'darwin') {
      const toIcns = join(__dirname, '..', 'build')
      const icns = runner('mk-icns', toIconPng, toIcns)
      promises.push(icns)
    }
    */
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
    const platform = `--${process.platform}`
    const target = process.argv[3]
    const args = [`electron:${action}`, platform, target]
    const cmd = `vue-cli-service${process.platform === 'win32' ? '.cmd' : '' }`
    runner(cmd, args)
  }


  if (action === 'postinstall') {
    const dependencies = {
      'win32': [
        'png-to-ico@2.1.8'
      ],
      'darwin': [
        'dmg-builder@24.0.0-alpha.3',
        'dmg-license@1.011',
        'make-icns@1.1.4'
      ]
    };

    if (dependencies[platform]) {
      console.log(`  \x1b[34m\u2022\x1b[0m installing dependent platform dependencies for ${platform}`)
      runner('yarn', ['add', dependencies[platform].join(' ')])
    } else {
      console.log(`  \x1b[34m\u2022\x1b[0m skipping dependent platform dependencies for ${platform}`)
    }
  }

  if (action === 'install-app-deps') {
    runner('electron-builder', [action])
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
