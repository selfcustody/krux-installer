export default (ms) => {
  return new Promise((resolve) => {
    return setTimeout(resolve, ms)
  })
}
