import request from '@/utils/request'
import type { Category } from '@/types'

export const getCategories = () =>
  request.get<any, Category[]>('/categories/')
