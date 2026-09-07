import request from '@/utils/request'
import type { OperationLog, PageResult } from '@/types'

export const listLogs = (params: { page?: number; page_size?: number; action?: string }) =>
  request.get<any, PageResult<OperationLog>>('/admin/logs', { params })
