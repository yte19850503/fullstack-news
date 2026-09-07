import { ref, watchEffect, onUnmounted } from 'vue'

interface SeoMeta {
  title?: string
  description?: string
  keywords?: string
  ogTitle?: string
  ogDescription?: string
  ogImage?: string
  ogType?: string
  ogUrl?: string
  jsonLd?: Record<string, any>
}

let jsonLdEl: HTMLScriptElement | null = null

export function useSeo(meta: SeoMeta | (() => SeoMeta)) {
  const refs: HTMLElement[] = []

  function setMeta(attr: string, value: string | undefined) {
    if (!value) return
    let el = document.querySelector(`meta[${attr}]`)
    if (!el) {
      el = document.createElement('meta')
      const [key] = attr.split('=')
      el.setAttribute(key, attr.split('=')[1]?.replace(/"/g, '') ?? key)
      document.head.appendChild(el)
    }
    const [key, val] = attr.split('=')
    el.setAttribute(key, val.replace(/"/g, ''))
    el.setAttribute('content', value)
    refs.push(el as HTMLElement)
  }

  function setJsonLd(data: Record<string, any>) {
    if (!jsonLdEl) {
      jsonLdEl = document.createElement('script')
      jsonLdEl.type = 'application/ld+json'
      document.head.appendChild(jsonLdEl)
    }
    jsonLdEl.textContent = JSON.stringify(data)
  }

  function cleanup() {
    refs.forEach((el) => {
      const name = el.getAttribute('name')
      const property = el.getAttribute('property')
      if (name) el.setAttribute('content', '')
      if (property) el.setAttribute('content', '')
    })
    refs.length = 0
    if (jsonLdEl) {
      jsonLdEl.remove()
      jsonLdEl = null
    }
  }

  watchEffect(() => {
    const resolved = typeof meta === 'function' ? meta() : meta

    if (resolved.title) {
      document.title = resolved.title
    }
    if (resolved.description) {
      setMeta('name="description"', resolved.description)
    }
    if (resolved.keywords) {
      setMeta('name="keywords"', resolved.keywords)
    }
    if (resolved.ogTitle) {
      setMeta('property="og:title"', resolved.ogTitle)
    }
    if (resolved.ogDescription) {
      setMeta('property="og:description"', resolved.ogDescription)
    }
    if (resolved.ogImage) {
      setMeta('property="og:image"', resolved.ogImage)
    }
    if (resolved.ogType) {
      setMeta('property="og:type"', resolved.ogType)
    }
    if (resolved.ogUrl) {
      setMeta('property="og:url"', resolved.ogUrl)
    }
    if (resolved.jsonLd) {
      setJsonLd(resolved.jsonLd)
    }
  })

  onUnmounted(cleanup)
}
