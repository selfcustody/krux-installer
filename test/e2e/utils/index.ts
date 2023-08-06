const { join } = require('path')
const { readFile } = require('fs/promises')
const { browser } = require('@wdio/globals')

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
