import { copyFile, readFile, mkdir, exists, unlink } from 'fs'
import { promisify } from 'util'

/**
 * Copy file in asynchronous manner
 *
 * @param origin<String>: the full path of origin file
 * @param destination<String>: the full path of destination file
 */
export const copyFileAsync = promisify(copyFile)

/**
 * Copy file in asynchronous manner
 *
 * @param origin<String>: the full path of origin file
 * @param destination<String>: the full path of destination file
 */
export const readFileAsync = promisify(readFile)

/*
 * Function to check if file or folder exists
 * in async/await approach. Always resoulves to
 * a boolean value.
 *
 * @param p<String>: path of the file
 * @return Boolean
 */
export const existsAsync = promisify(exists)

/*
 * Function to check if file or folder exists
 * in async/await approach. Always resoulves to
 * a boolean value.
 *
 * @param p<String>: path of the file
 * @return Boolean
 */
export const rmAsync = promisify(unlink)

/*
 * Function to create folder recursively
 * in async/await approach. Throws
 * an error if any occurs.
 *
 * @param p<String>: path of the file
 * @throw Error: if some error occurs
 */
export function mkdirAsync(p: string): Promise<void> {
  return new Promise((resolve, reject) => {
    mkdir(p, { recursive: true }, function(err) {
      if (err) reject(err)
      resolve()
    })
  })
}


/*
 * Function to format the size in bytes
 *
 * found at https://stackoverflow.com/questions/15900485/correct-way-to-convert-size-in-bytes-to-kb-mb-gb-in-javascript#18650828
 */
export function formatBytes(bytes, decimals: number = 2): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
} 
