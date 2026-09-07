export type ArticleStatus = 'DRAFT' | 'PUBLISHED' | 'ARCHIVED'

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface Category {
  id: number
  name: string
  slug: string
  description: string | null
}

export interface Tag {
  id: number
  name: string
  slug: string
}

export interface ArticleBrief {
  id: number
  title: string
  slug: string
  summary: string | null
  cover_image: string | null
  view_count: number
  created_at: string
  author: { id: number; name: string; avatar: string | null } | null
  category: { id: number; name: string; slug: string } | null
  tags: { id: number; name: string; slug: string }[]
}

export interface ArticleDetail extends ArticleBrief {
  content: string
  status: ArticleStatus
  updated_at: string
}

export interface Comment {
  id: number
  content: string
  article_id: number
  user_id: number
  parent_id: number | null
  created_at: string
  user: { id: number; name: string; avatar: string | null } | null
  replies: Comment[]
}

export interface AdPublic {
  id: number
  name: string
  position: string
  ad_type: string
  code: string
}

export interface UserLogin {
  email: string
  password: string
}

export interface UserInfo {
  id: number
  email: string
  name: string
  avatar: string | null
}
