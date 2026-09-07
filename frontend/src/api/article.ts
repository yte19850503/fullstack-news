import request from '@/utils/request'
import type { ArticleBrief, ArticleDetail, PageResult } from '@/types'

export const getArticles = (params: {
  page?: number
  page_size?: number
  category_id?: number
  status?: string
  q?: string
  tag_id?: number
  sort?: string
}) => request.get<any, PageResult<ArticleBrief>>('/articles/', { params })

export const getArticle = (slug: string) =>
  request.get<any, ArticleDetail>(`/articles/${slug}`)

export const searchArticles = (q: string, page = 1, page_size = 20) =>
  request.get<any, PageResult<ArticleBrief>>('/articles/search', { params: { q, page, page_size } })

export const getHotSearchTerms = (top = 10) =>
  request.get<any, { term: string; count: number }[]>('/articles/hot-search-terms', { params: { top } })
