import request from '@/utils/request'
import type { Comment } from '@/types'

export const getComments = (articleId: number) =>
  request.get<any, Comment[]>(`/comments/article/${articleId}`)

export const postComment = (articleId: number, content: string, parentId?: number) =>
  request.post<any, Comment>('/comments/', { article_id: articleId, content, parent_id: parentId ?? null })
