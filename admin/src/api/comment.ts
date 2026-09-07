import request from '@/utils/request'
import type { AdminComment, PageResult } from '@/types'

export const listComments = (params: { page?: number; page_size?: number; article_id?: number }) =>
  request.get<any, PageResult<AdminComment>>('/admin/comments', { params })

export const deleteComment = (id: number) =>
  request.delete(`/admin/comments/${id}`)
