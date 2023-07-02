import { Ref } from "vue"
import delay from "./delay"

export default async function addMessage(
  data: Ref<Record<string, any>>,
  message: string
): Promise<void> {
  data.value.messages.push(message)
  data.value.indexes.push(0)
  await delay(10)
  data.value.indexes[data.value.indexes.length - 1] += 1
  await delay(3000)
}