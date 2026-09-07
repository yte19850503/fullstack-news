import request from '@/utils/request'

export const login = (email: string, password: string) =>
  request.post<any, { token: string }>('/auth/login', { email, password })

export const logout = () => request.post('/auth/logout')
