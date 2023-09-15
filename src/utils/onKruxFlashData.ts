import { Ref } from "vue";

// If you have no problems simply ignoring all type-checking features for this library, you have two options:
// Add @ts-ignore above all imports or Create a declaration file with any type, so all imports are automatically considered to be of any type.
// see https://stackoverflow.com/questions/56688893/how-to-use-a-module-when-it-could-not-find-a-declaration-file#answer-56690386
// @ts-ignore
import { AnsiUp } from 'ansi_up'

/**
 * Stream shell output to web frontend
 * @see https://www.appsloveworld.com/vuejs/100/8/stream-shell-output-to-web-front-end
 * @param data
 */
export default function (
  data: Ref<Record<string, any>>
): Function {
  return function (
    _: Event, 
    result:string
  ): void {
    const ansi = new AnsiUp()
    let tmp = result.replace(/%\s/, "\n")
    tmp = tmp.replace(/kiB\/s/g, "kiB/s\n")

    data.value.output = ansi.ansi_to_html(tmp).replace(/\n/gm, '<br>')
  }
}
