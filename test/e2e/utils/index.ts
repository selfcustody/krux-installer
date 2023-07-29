const { join } = require('path')
const { readFile } = require('fs/promises')
const { browser } = require('@wdio/globals')

exports.getAPI = async function(): Promise<Record<string, any>> {
  return await browser.electron.api() as Record<string, any>
}

exports.getAppDataPath = async function (): Promise<string> {
  return await browser.electron.app('getPath', 'appData') as string
}

exports.getResourcesPath = async function (): Promise<string> {
  return await browser.electron.app('getPath', 'documents') as string
}

exports.getAppDataNamePath = async function (): Promise<string> {
  const api = await exports.getAPI()
  return join(api.appData, pkg.name)
}

exports.getConfigPath = async function (): Promise<string> {
  const appDataNamePath = await exports.appDataNamePath()
  return join(appDataNamePath, 'config.json')
}

exports.getConfigString = async function (): Promise<string> {
  const configPath = await exports.getConfigPath()
  return await readFile(configPath, 'utf8')
}

exports.getConfigObject = async function (): Promise<Record<string, any>> {
  const configString = await exports.getConfigString()
  return JSON.parse(configString)
}

exports.isAppReady = async function (): Promise<boolean> {
  return await browser.electron.app('isReady') as boolean
}

exports.getAppName = async function (): Promise<string> {
  return await browser.electron.app('getName') as string
}

exports.getAppVersion = async function  (): Promise<string> {
  return await browser.electron.app('getVersion') as string
}

exports.delay = function (ms: number): Promise<number> {
  return new Promise((resolve) => {
    return setTimeout(resolve, ms)
  })
}

// Correct way to convert size in bytes to KB, MB, GB in JavaScript
// https://gist.github.com/lanqy/5193417?permalink_comment_id=4225701#gistcomment-4225701
exports.formatBytes = function (bytes: number): string {
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  if (bytes === 0) return 'n/a'
  const n = Math.log(bytes as number) / Math.log(1024)
  const i = Math.min(Math.floor(n), sizes.length - 1)
  if (i === 0) return `${bytes} ${sizes[i]}`
  return `${(bytes / (1024 ** i)).toFixed(2)} ${sizes[i]}` as string
}
