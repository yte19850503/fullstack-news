import request from '@/utils/request'
import type { Tag } from '@/types'

export const getTags = () =>
  request.get<any, Tag[]>('/tags/')
