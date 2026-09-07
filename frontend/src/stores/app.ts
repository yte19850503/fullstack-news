import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getCategories } from '@/api/category'
import { getTags } from '@/api/tag'
import type { Category, Tag } from '@/types'

export const useAppStore = defineStore('app', () => {
  const categories = ref<Category[]>([])
  const tags = ref<Tag[]>([])
  const loaded = ref(false)

  async function loadBaseData() {
    if (loaded.value) return
    const [cats, tg] = await Promise.all([getCategories(), getTags()])
    categories.value = cats
    tags.value = tg
    loaded.value = true
  }

  return { categories, tags, loaded, loadBaseData }
})
