import { Ref } from "vue";

/**
 * Stream shell output to web frontend
 * @see https://www.appsloveworld.com/vuejs/100/8/stream-shell-output-to-web-front-end
 * @param data
 */
export default function (
  data: Ref<Record<string, any>>
): Function {
  return async function (
    _: Event, 
    result:Record<'will', string>
  ): Promise<void>{
    console.log("DATA===============")
    console.log(data)
    console.log("RESULT===============")
    console.log(result)
    if (result.will == 'flash') {
      await window.api.invoke('krux:flash')
    } else if (result.will == 'wipe') {
      await window.api.invoke('krux:wipe')
    }
  }
}
