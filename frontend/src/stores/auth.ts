import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { login as apiLogin, register as apiRegister } from '@/api/auth'
import type { UserInfo } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(getToken())
  const user = ref<UserInfo | null>(null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(email: string, password: string) {
    const res = await apiLogin(email, password)
    token.value = res.token
    setToken(res.token)
  }

  async function register(email: string, password: string, name: string) {
    const res = await apiRegister(email, password, name)
    token.value = res.token
    setToken(res.token)
  }

  function logout() {
    token.value = ''
    user.value = null
    removeToken()
  }

  return { token, user, isLoggedIn, login, register, logout }
})
