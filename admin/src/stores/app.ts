import { ref } from 'vue'
import { defineStore } from 'pinia'

const COLLAPSED_KEY = 'sidebar_collapsed'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(localStorage.getItem(COLLAPSED_KEY) === 'true')

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
    localStorage.setItem(COLLAPSED_KEY, String(sidebarCollapsed.value))
  }

  return { sidebarCollapsed, toggleSidebar }
})
