import { rmSync } from 'node:fs'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import electron from 'vite-plugin-electron'
import { createHtmlPlugin } from 'vite-plugin-html'


//import renderer from 'vite-plugin-electron-renderer'
import pkg from './package.json'

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  rmSync('dist-electron', { recursive: true, force: true })

  const isServe = command === 'serve'
  const isBuild = command === 'build'
  const sourcemap = isServe || !!process.env.VSCODE_DEBUG

  return {
    open: true,
    plugins: [
      vue(),
      vuetify({ autoImport: true }),
      electron([
        {
          entry: 'electron/main/index.ts',
          onstart(options) {
            
            /* See `.vscode/.debug.script.mjs` */
            if (process.env.VSCODE_DEBUG) {
              console.log(`[ startup ] KruxInstaller v${pkg.version}`)
            } else {
              options.startup()
            }
          },
          vite: {
            build: {
              sourcemap,
              minify: isBuild,
              outDir: 'dist-electron/main',
              rollupOptions: {
                external: Object.keys('dependencies' in pkg ? pkg.dependencies : {}),
              },
            },
          }
        },
        {
          entry: 'electron/preload/index.ts',
          onstart(options) {
            // Notify the Renderer-Process to reload the page when the Preload-Scripts build is complete, 
            // instead of restarting the entire Electron App.
            if (process.env.VSCODE_DEBUG) {
              console.log(`[ reload ] KruxInstaller v${pkg.version}`)
            } else {
              options.reload()
            }
          },
          vite: {
            build: {
              sourcemap: sourcemap ? 'inline' : undefined, // #332
              minify: isBuild,
              outDir: 'dist-electron/preload',
              rollupOptions: {
                external: Object.keys('dependencies' in pkg ? pkg.dependencies : {}),
              },
            },
          }
        }
      ]),
      createHtmlPlugin({
        minify: true,
        inject: {
          data: {
            title: `${pkg.name} ${pkg.version}`
          }
        }
      })
    ],
    server: process.env.VSCODE_DEBUG && (() => {
      const url = new URL(pkg.vscode.debug.env.VITE_DEV_SERVER_URL)
      return {
        host: url.hostname,
        port: +url.port,
      }
    })(),
    clearScreen: false,
  }
})
