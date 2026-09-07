import request from '@/utils/request'

export const login = (email: string, password: string) =>
  request.post<any, { token: string }>('/auth/login', { email, password })

export const register = (email: string, password: string, name: string) =>
  request.post<any, { token: string }>('/auth/register', { email, password, name })
