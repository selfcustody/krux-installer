import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createRequire } from 'node:module'
import { spawn } from 'node:child_process'

const pkg = createRequire(import.meta.url)('../package.json')
const __dirname = path.dirname(fileURLToPath(import.meta.url))

// parse .script.mjs option to create an
// appropriate .env file
const option = process.argv[2]

// write .debug.env
const envContent = Object.entries(pkg.vscode[option].env).map(([key, val]) => `${key}=${val}`)
const envName = `.${option}.env`
const envPath = path.join(__dirname, envName)
console.log(`Creating ${envPath}`)
fs.writeFileSync(envPath, envContent.join('\n'))

const runCommand = pkg.vscode[option].run.split(' ')

// bootstrap
spawn(
  // TODO: terminate `npm run dev` when Debug exits.
  process.platform === 'win32' ? `${runCommand[0]}.cmd` : runCommand[0],
  [runCommand[1], runCommand[2]],
  {
    stdio: 'inherit',
    env: Object.assign(process.env, { VSCODE_DEBUG: 'true' }),
  },
)
