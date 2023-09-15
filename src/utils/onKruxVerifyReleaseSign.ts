import { Ref } from "vue"

/**
 * Store result of signature verification
 * (and its command)  in `data`, then redirect to
 * VerifiedOfficialRelease page
 * @param data 
 * @returns Function
 */
export default function (data: Ref<Record<string, any>>): Function {
  return async function onKruxVerifyReleaseSign (_: Event, result: Record<'command' | 'sign', any>): Promise<void> {
    data.value.command = result.command
    data.value.sign = result.sign
    await window.api.invoke('krux:change:page', { page: 'VerifiedOfficialRelease' })
  }
}