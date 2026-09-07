import request from '@/utils/request'
import type { AdPublic } from '@/types'

export const getPublicAds = (position: string) =>
  request.get<any, AdPublic[]>('/ads/public', { params: { position } })

export const recordAdEvent = (slotId: number, event: 'impression' | 'click') =>
  request.post(`/ads/public/${slotId}/event`, null, { params: { event } })
