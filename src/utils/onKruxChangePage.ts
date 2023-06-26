import { Ref } from "vue"

/**
 * Simple function to change pages
 * @param page 
 * @returns Function
 */
export default function (page: Ref<string>): Function {
  return function (_: Event, result: Record<'page', string>) {
    page.value = result.page
  }
}