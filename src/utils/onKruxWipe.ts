import { Ref } from "vue";

export default function (
  data: Ref<Record<string, any>>
): Function {
  return function (
    _: Event, 
    result:Record<string, any>
  ): void {
    data.value.done = result.done
  }
}
