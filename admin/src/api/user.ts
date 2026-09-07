import request from '@/utils/request'
import type { AdminUser, PageResult } from '@/types'

export const listUsers = (params: { page?: number; page_size?: number; role?: string; q?: string }) =>
  request.get<any, PageResult<AdminUser>>('/admin/users', { params })

export const updateUser = (id: number, data: { name?: string; role?: string }) =>
  request.put<any, AdminUser>(`/admin/users/${id}`, data)

export const toggleUserActive = (id: number, is_active: boolean) =>
  request.put(`/admin/users/${id}/toggle-active`, { is_active })
