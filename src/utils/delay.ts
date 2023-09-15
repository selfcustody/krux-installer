export default async function delay (t: number) {
  await new Promise(function (resolve) {
    setTimeout(resolve, t)
  })
}