import { join } from 'path'
import { access, readFile } from 'fs'
import { promisify } from 'util'
import { browser } from 'wdio-electron-service'
import { createRequire } from 'node:module'

const { name } = createRequire(import.meta.url)('../../../package.json')

export const existsAsync = promisify(access)
export const readFileAsync = promisify(readFile)

export async function getAPI (): Promise<Record<string, any>> {
  return await browser.electron.api() as Record<string, any>
}

export async function getAppDataPath (): Promise<string> {
  return await browser.electron.app('getPath', 'appData') as string
}

export async function getResourcesPath (): Promise<string> {
  return await browser.electron.app('getPath', 'documents') as string
}

export async function getAppDataNamePath (): Promise<string> {
  const api = await getAPI()
  return join(api.appData, name)
}

export async function getConfigPath (): Promise<string> {
  const appDataNamePath = await getAppDataNamePath()
  return join(appDataNamePath, 'config.json')
}

export async function getConfigString (): Promise<string> {
  const configPath = await getConfigPath()
  return await readFileAsync(configPath, 'utf8')
}

export async function getConfigObject (): Promise<Record<string, any>> {
  const configString = await getConfigString()
  return JSON.parse(configString)
}

export async function isAppReady (): Promise<boolean> {
  return await browser.electron.app('isReady') as boolean
}

export async function getAppName (): Promise<string> {
  return await browser.electron.app('getName') as string
}

export async function getAppVersion (): Promise<string> {
  return await browser.electron.app('getVersion') as string
}

export function delay(ms: number): Promise<number> {
  return new Promise((resolve) => {
    return setTimeout(resolve, ms)
  })
}

// Correct way to convert size in bytes to KB, MB, GB in JavaScript
// https://gist.github.com/lanqy/5193417?permalink_comment_id=4225701#gistcomment-4225701
export function formatBytes (bytes: number, aproximation: string ='floor') {
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  if (bytes === 0) return 'n/a'
  const i = Math.min(Math[aproximation](Math.log(bytes) / Math.log(1024)), sizes.length - 1)
  if (i === 0) return `${bytes} ${sizes[i]}`
  return `${(bytes / (1024 ** i)).toFixed(2)} ${sizes[i]}`
}
