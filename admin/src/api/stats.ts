import request from '@/utils/request'
import type { Stats } from '@/types'

export const getStats = () => request.get<any, Stats>('/admin/stats')
