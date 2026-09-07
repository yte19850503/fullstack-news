import request from '@/utils/request'
import type { AdminArticle, ArticleStatus, PageResult, Category, Tag } from '@/types'

export const listArticles = (params: { page?: number; page_size?: number; status?: string; q?: string }) =>
  request.get<any, PageResult<AdminArticle>>('/admin/articles', { params })

export const getArticle = (id: number) =>
  request.get<any, ArticleDetail>(`/admin/articles/${id}`)

export const createArticle = (data: ArticleFormData) =>
  request.post<any, ArticleDetail>('/admin/articles', data)

export const updateArticle = (id: number, data: Partial<ArticleFormData>) =>
  request.put<any, ArticleDetail>(`/admin/articles/${id}`, data)

export const deleteArticle = (id: number) =>
  request.delete(`/admin/articles/${id}`)

export const reviewArticle = (id: number, status: ArticleStatus) =>
  request.put(`/admin/articles/${id}/review`, null, { params: { status } })

export const batchUpdateArticles = (ids: number[], status: ArticleStatus) =>
  request.post('/admin/articles/batch-update', ids, { params: { status } })

export const getCategories = () =>
  request.get<any, Category[]>('/admin/categories')

export const getTags = () =>
  request.get<any, Tag[]>('/admin/tags')

export interface ArticleFormData {
  title: string
  content: string
  summary?: string
  cover_image?: string
  category_id: number
  tag_ids?: number[]
  status?: ArticleStatus
}

export interface ArticleDetail extends AdminArticle {
  content: string
  summary: string | null
  cover_image: string | null
  author: { id: number; name: string; avatar: string | null } | null
  category: { id: number; name: string; slug: string } | null
  tags: { id: number; name: string; slug: string }[]
  created_at: string
  updated_at: string
}
