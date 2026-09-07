import type { JwtPayload } from '@/types'

const TOKEN_KEY = 'admin_token'

export const getToken = (): string => localStorage.getItem(TOKEN_KEY) ?? ''

export const setToken = (token: string) => localStorage.setItem(TOKEN_KEY, token)

export const removeToken = () => localStorage.removeItem(TOKEN_KEY)

export function parseJwt(token: string): JwtPayload | null {
  try {
    const payload = token.split('.')[1]
    const json = atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
    return JSON.parse(json)
  } catch {
    return null
  }
}
