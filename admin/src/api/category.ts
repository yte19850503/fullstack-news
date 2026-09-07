import request from '@/utils/request'
import type { Category } from '@/types'

export const listCategories = () =>
  request.get<any, Category[]>('/admin/categories')

export const createCategory = (name: string, description?: string) =>
  request.post<any, Category>('/admin/categories', null, { params: { name, description } })

export const updateCategory = (id: number, name?: string, description?: string) =>
  request.put<any, Category>(`/admin/categories/${id}`, null, { params: { name, description } })

export const deleteCategory = (id: number) =>
  request.delete(`/admin/categories/${id}`)
