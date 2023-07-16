import { Ref } from "vue";
import AnsiUp from "ansi_up";

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
    data.value.output = result.replace(/%\s/, "\n")
    data.value.output = data.value.output.replace(/kiB\/s/g, "kiB/s\n")
      
    const ansi = new AnsiUp()
    data.value.output = ansi.ansi_to_html(data.value.output).replace(/\n/gm, '<br>')
  }
}
