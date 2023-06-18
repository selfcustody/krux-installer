export default async function (
  result: Record<'from', string>,
  options: Record<'from' | 'to', string>
): Promise<void> {
  if (result.from === options.from) {
    await window.api.invoke('krux:change:page', { page: options.to })
  }
} 