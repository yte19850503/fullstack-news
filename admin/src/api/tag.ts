import request from '@/utils/request'
import type { Tag } from '@/types'

export const listTags = () =>
  request.get<any, Tag[]>('/admin/tags')

export const createTag = (name: string, slug: string) =>
  request.post<any, Tag>('/admin/tags', { name, slug })

export const updateTag = (id: number, data: { name?: string; slug?: string }) =>
  request.put<any, Tag>(`/admin/tags/${id}`, data)

export const deleteTag = (id: number) =>
  request.delete(`/admin/tags/${id}`)
