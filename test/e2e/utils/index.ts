import { join } from 'path'
import { access, readFile } from 'fs'
import { promisify } from 'util'
import { browser } from 'wdio-electron-service';
import { name } from '../../../package.json';

export const existsAsync = promisify(access)
const readFileAsync = promisify(readFile)

export async function getAPI (): Promise<Record<string, any>> {
  return await browser.electron.api() as Record<string, any>
}

export async function getAppDataPath (): Promise<string> {
  const api = await getAPI()
  return api.appData
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
