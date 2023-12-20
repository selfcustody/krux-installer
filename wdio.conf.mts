import { join, dirname } from 'path'
import { fileURLToPath } from 'url';
import { glob, globSync } from 'glob'
import { rimraf } from 'rimraf'
import { tmpdir, homedir } from 'os'
import { createRequire } from 'module'
import { osLangSync } from 'os-lang'
import createDebug from 'debug'
import { accessSync } from 'fs';
import { exec, execFile } from 'child_process';

const { devDependencies, version } = createRequire(import.meta.url)('./package.json')
const debug = createDebug('krux:wdio:e2e')
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// select the correct binary
// for each OS
let APP_PATH: string
if (process.platform === 'linux') {
  APP_PATH = join(__dirname, 'release', version, 'linux-unpacked', 'krux-installer')
} else if (process.platform === 'win32') {
  APP_PATH = join(__dirname, 'release', version, 'win-unpacked', 'krux-installer.exe')
} else if (process.platform === 'darwin') {
  APP_PATH = join(__dirname, 'release', version, 'mac', 'krux-installer.app', 'Contents', 'MacOS', 'krux-installer')
} else {
  throw new Error(`Platform '${process.platform}' not implemented`)
}

const APP_ARGS = [
  '--disable-infobars',
  '--disable-dev-shm-usage',
  '--no-sandbox',
  '--remote-debugging-port=9222'
]

// Define which specs to
// test or to exclude
let SPECS_TO_TEST: string[] = [];
let SPECS_TO_EXCLUDE: string[] = [];

// Prepare resources path
// for specific test environment
let resources = ''
  
if (process.env.CI && process.env.GITHUB_ACTION) {
  if (process.platform  === 'linux') {
    resources = '/home/runner/krux-installer'
  } else if (process.platform  === 'win32') {
    resources = 'C:\\Users\\runneradmin\\Documents\\krux-installer'
  } else if (process.platform  === 'darwin') {
    resources = '/Users/runner/Documents/krux-installer'
  }
} else {
  const lang = osLangSync()
  const home = homedir()
  if ( lang.match(/en-*/g)) {
    resources = join(home, 'Documents', 'krux-installer')
  } else if ( lang.match(/pt-*/g)) {
    resources = join(home, 'Documentos', 'krux-installer')
  } else {
    throw new Error(`${lang} not implemented. Please implement it with correct \'Documents\' folder name`)
  }
}

// Define where specs are located
const specs = globSync('./test/e2e/specs/*.spec.mts')

// If you want to filter some test, you could use
// a `--filter` with regular expression
const hasFilter = process.argv.slice(4)

if (hasFilter.length > 0) {
  
  if (hasFilter[0] === '--filter' || hasFilter[0] === '-f') {
    const filter = new RegExp(hasFilter[1], 'g')
    specs.map(async function (file: string) {
      if (file.match(filter)) {
        debug(`Excluding ${file}`)
        SPECS_TO_EXCLUDE.push(file)
      }
    })
  }
}

// loop through all specs and verify
// if some of them could have a resource test.
// - Positive: add it to SPECS_TO_EXCLUDE
// - Negative: add it to SPECS_TO_TEST
specs.map(async function (file: string) {
  if (
    file === 'test/e2e/specs/014.select-version-selfcustody-release-zip.spec.ts' ||
    file === 'test/e2e/specs/018.already-downloaded-selfcustody-release-zip-click-download-again.spec.ts' 
  ) {
    try {
      const r = join(resources, 'v22.08.2', 'krux-v22.08.2.zip')
      accessSync(r)
      SPECS_TO_EXCLUDE.push(file)
    } catch (error) {
      SPECS_TO_TEST.push(file)
    }
  } else if (
    file === 'test/e2e/specs/020.select-version-selfcustody-release-zip-sha256.spec.ts' ||
    file === 'test/e2e/specs/024.already-downloaded-selfcustody-release-zip-sha256-click-download-again-button.spec.ts'
  ) {
    try {
      const r = join(resources, 'v22.08.2', 'krux-v22.08.2.zip.sha256.txt')
      accessSync(r)
      SPECS_TO_EXCLUDE.push(file)
    } catch (error) {
      SPECS_TO_TEST.push(file)
    }
  } else if (
    file === 'test/e2e/specs/026.select-version-selfcustody-release-zip-sig.spec.ts' ||
    file === 'test/e2e/specs/030.already-downloaded-selfcustody-release-zip-sig-download-again-button.spec.ts'
  ) {
    try {
      const r = join(resources, 'v22.08.2', 'krux-v22.08.2.zip.sig')
      accessSync(r)
      SPECS_TO_EXCLUDE.push(file)
    } catch (error) {
      SPECS_TO_TEST.push(file)
    }
  } else if (
    file === 'test/e2e/specs/032-select-version-selfcustody-pem.spec.ts'
  ) {
    try {
      const r = join(resources, 'main', 'selfcustody.pem')
      accessSync(r)
      SPECS_TO_EXCLUDE.push(file)
    } catch (error) {
      SPECS_TO_TEST.push(file)
    }
  }
  else {
    SPECS_TO_TEST.push(file)
  }
})

export const config = {
    //
    // ====================
    // Runner Configuration
    // ====================
    // WebdriverIO supports running e2e tests as well as unit and component tests.
    runner: 'local',
    //
    // ==================
    // Specify Test Files
    // ==================
    // Define which test specs should run. The pattern is relative to the directory
    // from which `wdio` was called.
    //
    // The specs are defined as an array of spec files (optionally using wildcards
    // that will be expanded). The test for each spec file will be run in a separate
    // worker process. In order to have a group of spec files run in the same worker
    // process simply enclose them in an array within the specs array.
    //
    // If you are calling `wdio` from an NPM script (see https://docs.npmjs.com/cli/run-script),
    // then the current working directory is where your `package.json` resides, so `wdio`
    // will be called from there.
    //
    specs: SPECS_TO_TEST.reverse(),
    //featureFlags: {
    //  specFiltering: true  
    //},
    // Patterns to exclude.
    exclude: SPECS_TO_EXCLUDE.reverse(),
    // WebdriverIO will automatically detect if these dependencies are installed
    // and will compile your config and tests for you. Ensure to have a tsconfig.json
    // in the same directory as you WDIO config. If you need to configure how ts-node
    // runs please use the environment variables for ts-node or use wdio config's
    // autoCompileOpts section.
    autoCompileOpts: {
      autoCompile: true,
      // see https://github.com/TypeStrong/ts-node#cli-and-programmatic-options
      // for all available options
      tsNodeOpts: {
        project: './tsconfig.e2e.json',
        transpileOnly: true,
      }
    },
    //
    // ============
    // Capabilities
    // ============
    // Define your capabilities here. WebdriverIO can run multiple capabilities at the same
    // time. Depending on the number of capabilities, WebdriverIO launches several test
    // sessions. Within your capabilities you can overwrite the spec and exclude options in
    // order to group specific specs to a specific capability.
    //
    // First, you can define how many instances should be started at the same time. Let's
    // say you have 3 different capabilities (Chrome, Firefox, and Safari) and you have
    // set maxInstances to 1; wdio will spawn 3 processes. Therefore, if you have 10 spec
    // files and you set maxInstances to 10, all spec files will get tested at the same time
    // and 30 processes will get spawned. The property handles how many capabilities
    // from the same test should run tests.
    //
    maxInstances: 1,
    //
    // If you have trouble getting all constant capabilities together, check out the
    // Sauce Labs platform configurator - a great tool to configure your capabilities:
    // https://saucelabs.com/platform/platform-configurator
    //
    capabilities: [{
        // maxInstances can get overwritten per capability. So if you have an in-house Selenium
        // grid with only 5 firefox instances available you can make sure that not more than
        // 5 instances get started at a time.
        maxInstances: 1,
        browserName: 'electron',
        'wdio:electronServiceOptions': {
          appBinaryPath: APP_PATH,
          appArgs: APP_ARGS,
        }
    }],
    //
    // ===================
    // Test Configurations
    // ===================
    // Define all options that are relevant for the WebdriverIO instance here
    //
    // Level of logging verbosity: trace | debug | info | warn | error | silent
    logLevel: 'trace',
    //
    // Set specific log levels per logger
    // loggers:
    // - webdriver, webdriverio
    // - @wdio/browserstack-service, @wdio/devtools-service, @wdio/sauce-service
    // - @wdio/mocha-framework, @wdio/jasmine-framework
    // - @wdio/local-runner
    // - @wdio/sumologic-reporter
    // - @wdio/cli, @wdio/config, @wdio/utils
    // Level of logging verbosity: trace | debug | info | warn | error | silent
    // logLevels: {
    //     webdriver: 'info',
    //     '@wdio/appium-service': 'info'
    // },
    //
    // If you only want to run your tests until a specific amount of tests have failed use
    // bail (default is 0 - don't bail, run all tests).
    bail: 1,
    //
    // Set a base URL in order to shorten url command calls. If your `url` parameter starts
    // with `/`, the base url gets prepended, not including the path portion of your baseUrl.
    // If your `url` parameter starts without a scheme or `/` (like `some/path`), the base url
    // gets prepended directly.
    baseUrl: 'http://localhost',
    //
    // Default timeout for all waitFor* commands.
    waitforTimeout: 10000,
    //
    // Default timeout in milliseconds for request
    // if browser driver or grid doesn't send response
    connectionRetryTimeout: 120000,
    //
    // Default request retries count
    connectionRetryCount: 3,
    //
    // Test runner services
    // Services take over a specific job you don't want to take care of. They enhance
    // your test setup with almost no effort. Unlike plugins, they don't add new
    // commands. Instead, they hook themselves up into the test process.
    services: ['electron'],
    // Framework you want to run your specs with.
    // The following are supported: Mocha, Jasmine, and Cucumber
    // see also: https://webdriver.io/docs/frameworks
    //
    // Make sure you have the wdio adapter package for the specific framework installed
    // before running any tests.
    framework: 'mocha',
    //
    // The number of times to retry the entire specfile when it fails as a whole
    // specFileRetries: 1,
    //
    // Delay in seconds between the spec file retry attempts
    // specFileRetriesDelay: 0,
    //
    // Whether or not retried specfiles should be retried immediately or deferred to the end of the queue
    // specFileRetriesDeferred: false,
    //
    // Test reporter for stdout.
    // The only one supported by default is 'dot'
    // see also: https://webdriver.io/docs/dot-reporter
    reporters: ['spec'],
    //
    // Options to be passed to Mocha.
    // See the full list at http://mochajs.org/
    mochaOpts: {
      ui: 'bdd',
      timeout: 600000,
      require: ['node_modules/@babel/register/lib/index.js']
    },
    //
    // =====
    // Hooks
    // =====
    // WebdriverIO provides several hooks you can use to interfere with the test process in order to enhance
    // it and to build services around it. You can either apply a single function or an array of
    // methods to it. If one of them returns with a promise, WebdriverIO will wait until that promise got
    // resolved to continue.
    /**
     * Gets executed once before all workers get launched.
     * @param {Object} config wdio configuration object
     * @param {Array.<Object>} capabilities list of capabilities details
     */
    //onPrepare: function (config, capabilities) {
    //},
    /**
     * Gets executed before a worker process is spawned and can be used to initialise specific service
     * for that worker as well as modify runtime environments in an async fashion.
     * @param  {String} cid      capability id (e.g 0-0)
     * @param  {[type]} caps     object containing capabilities for session that will be spawn in the worker
     * @param  {[type]} specs    specs to be run in the worker process
     * @param  {[type]} args     object that will be merged with the main configuration once worker is initialized
     * @param  {[type]} execArgv list of string arguments passed to the worker process
     */
    onWorkerStart: function (cid: string, caps: any, specs: any, args: any, execArgv: any) {
      // This is a little 'hacking'
      // the created 'krux-installer' process generated by
      // webdriveIO do not properly create the store
      // so we will run an no-test 'krux-installer'
      // that create the store, kill it
      // and then start to test
      return new Promise<void>(async function(resolve, reject) {
        if (specs[0].indexOf('000.create-config.spec.mts') !== -1) {
          const shell = process.env.SHELL
          debug(`platform: ${process.platform}`)
          debug(`shell: ${shell}`)
          debug('INTERMEDIATE RUNNING TO CREATE STORE')

          // Get the Process ID to stop it after exection
          debug(`exec: ${APP_PATH}`)
          debug(`args: ${APP_ARGS.join(' ')}`)
          const app = execFile(APP_PATH, APP_ARGS)
          debug(`PID ${app.pid}`)
          
          // Wait for some time, show the config file path
          // and stop the process killing it providing it pid.
          // Linux and darwin have similar ways to do this (`kill` command);
          // on windows, we will use powershell `Stop-Process -Id` arg
          // TODO: provide a cmd alternative on windows without powershell
          let store = ''
          let killCmd = ''
          if (process.platform === 'linux') {
            store = join(process.env.HOME as string, '.config', 'krux-installer')
            killCmd = `kill ${app.pid}`
          } else if (process.platform === 'win32') {
            store = join(process.env.APPDATA as string, 'krux-installer')
          } else if (process.platform === 'darwin') {
            store = join(process.env.HOME as string, 'Library', 'Application Support', 'krux-installer')
            killCmd = `Stop-Process -Id ${app.pid}`
          }

          setTimeout(function () {
            exec(killCmd, function(err) {
              if (err) {
                debug(err)
                reject(err)
              }
              debug(`killed process ${app.pid}`)
              resolve()
            })
          }, 10000)
          
        } else {
          resolve()
        }
      })
    },
    /**
     * Gets executed just after a worker process has exited.
     * @param  {String} cid      capability id (e.g 0-0)
     * @param  {Number} exitCode 0 - success, 1 - fail
     * @param  {[type]} specs    specs to be run in the worker process
     * @param  {Number} retries  number of retries used
     */
    // onWorkerEnd: function (cid, exitCode, specs, retries) {
    // },
    /**
     * Gets executed just before initialising the webdriver session and test framework. It allows you
     * to manipulate configurations depending on the capability or spec.
     * @param {Object} config wdio configuration object
     * @param {Array.<Object>} capabilities list of capabilities details
     * @param {Array.<String>} specs List of spec file paths that are to be run
     * @param {String} cid worker id (e.g. 0-0)
     */
    // beforeSession: function (config, capabilities, specs, cid) {
    // },
    /**
     * Gets executed before test execution begins. At this point you can access to all global
     * variables like `browser`. It is the perfect place to define custom commands.
     * @param {Array.<Object>} capabilities list of capabilities details
     * @param {Array.<String>} specs        List of spec file paths that are to be run
     * @param {Object}         browser      instance of created browser/device session
     */
    // before: function (capabilities, specs) {
    // },
    /**
     * Runs before a WebdriverIO command gets executed.
     * @param {String} commandName hook command name
     * @param {Array} args arguments that command would receive
     */
    // beforeCommand: function (commandName, args) {
    // },
    /**
     * Hook that gets executed before the suite starts
     * @param {Object} suite suite details
     */
    // beforeSuite: function (suite) {
    // },
    /**
     * Function to be executed before a test (in Mocha/Jasmine) starts.
     */
    // beforeTest: function (test, context) {
    // },
    /**
     * Hook that gets executed _before_ a hook within the suite starts (e.g. runs before calling
     * beforeEach in Mocha)
     */
    //beforeHook: function (test, context) {
    // },
    /**
     * Hook that gets executed _after_ a hook within the suite starts (e.g. runs after calling
     * afterEach in Mocha)
     */
    // afterHook: function (test, context, { error, result, duration, passed, retries }) {
    // },
    /**
     * Function to be executed after a test (in Mocha/Jasmine only)
     * @param {Object}  test             test object
     * @param {Object}  context          scope object the test was executed with
     * @param {Error}   result.error     error object in case the test fails, otherwise `undefined`
     * @param {Any}     result.result    return object of test function
     * @param {Number}  result.duration  duration of test
     * @param {Boolean} result.passed    true if test has passed, otherwise false
     * @param {Object}  result.retries   informations to spec related retries, e.g. `{ attempts: 0, limit: 0 }`
     */
    // afterTest: function(test, context, { error, result, duration, passed, retries }) {
    // },
    /**
     * Hook that gets executed after the suite has ended
     * @param {Object} suite suite details
     */
    //afterSuite: async function (suite) {
    //},
    /**
     * Runs after a WebdriverIO command gets executed
     * @param {String} commandName hook command name
     * @param {Array} args arguments that command would receive
     * @param {Number} result 0 - command success, 1 - command error
     * @param {Object} error error object if any
     */
    // afterCommand: function (commandName, args, result, error) {
    // },
    /**
     * Gets executed after all tests are done. You still have access to all global variables from
     * the test.
     * @param {Number} result 0 - test pass, 1 - test fail
     * @param {Array.<Object>} capabilities list of capabilities details
     * @param {Array.<String>} specs List of spec file paths that ran
     */
    // after: function (result, capabilities, specs) {
    // },
    /**
     * Gets executed right after terminating the webdriver session.
     * @param {Object} config wdio configuration object
     * @param {Array.<Object>} capabilities list of capabilities details
     * @param {Array.<String>} specs List of spec file paths that ran
     */
    // afterSession: function (config, capabilities, specs) {
    // },
    /**
     * Gets executed after all workers got shut down and the process is about to exit. An error
     * thrown in the onComplete hook will result in the test run failing.
     * @param {Object} exitCode 0 - success, 1 - fail
     * @param {Object} config wdio configuration object
     * @param {Array.<Object>} capabilities list of capabilities details
     * @param {<Object>} results object containing test results
     */
    // eslint-disable-next-line no-unused-vars
    onComplete: async function(exitCode: number, config: Object, capabilities: Object[], results: Object) {

      async function removing(dir: string) {
        debug(`Cleaning ${dir}`)
        try {
          await rimraf(dir, { preserveRoot: false })
          debug(`${dir} removed`)
        } catch (error) {
          debug(error)
        }
      }

      const tmp = tmpdir()
      const yarnDir = join(tmp, 'yarn--*')
      const lightDir = join(tmp, 'lighthouse.*')
      const yarns = await glob(yarnDir)
      const lights = await glob(lightDir)
      yarns.map(removing)
      lights.map(removing)
    },
    /**
    * Gets executed when a refresh happens.
    * @param {String} oldSessionId session ID of the old session
    * @param {String} newSessionId session ID of the new session
    */
    // onReload: function(oldSessionId, newSessionId) {
    // }
}
