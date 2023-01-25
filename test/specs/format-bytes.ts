// Correct way to convert size in bytes to KB, MB, GB in JavaScript
// https://gist.github.com/lanqy/5193417?permalink_comment_id=4225701#gistcomment-4225701
export default function (bytes) {
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  if (bytes === 0) return 'n/a'
  const i = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), sizes.length - 1)
  if (i === 0) return `${bytes} ${sizes[i]}`
  return `${(bytes / (1024 ** i)).toFixed(1)} ${sizes[i]}`
}
