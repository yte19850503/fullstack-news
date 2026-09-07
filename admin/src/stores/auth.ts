import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { getToken, setToken, removeToken, parseJwt } from '@/utils/auth'
import { login as loginApi, logout as logoutApi } from '@/api/auth'
import type { JwtPayload } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(getToken())

  const user = computed<JwtPayload | null>(() =>
    token.value ? parseJwt(token.value) : null,
  )

  const isLoggedIn = computed(() =>
    !!token.value && !!user.value && user.value.exp * 1000 > Date.now(),
  )

  const isAdmin = computed(() => user.value?.role === 'ADMIN')

  async function login(email: string, password: string) {
    const res = await loginApi(email, password)
    token.value = res.token
    setToken(res.token)
  }

  async function logout() {
    try {
      await logoutApi()
    } catch {
      // token may already be invalid
    }
    token.value = ''
    removeToken()
  }

  return { token, user, isLoggedIn, isAdmin, login, logout }
})
