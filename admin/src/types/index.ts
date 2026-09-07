export type Role = 'READER' | 'EDITOR' | 'ADMIN'
export type ArticleStatus = 'DRAFT' | 'PUBLISHED' | 'ARCHIVED'

export interface JwtPayload {
  sub: string
  email: string
  role: Role
  exp: number
}

export interface AdminUser {
  id: number
  email: string
  name: string
  role: Role
  is_active: boolean
  avatar: string | null
  created_at: string
}

export interface AdminArticle {
  id: number
  title: string
  slug: string
  status: ArticleStatus
  view_count: number
  created_at: string
  author_name: string | null
  category_name: string | null
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

export interface AdminComment {
  id: number
  content: string
  article_id: number
  user_id: number
  parent_id: number | null
  created_at: string
  user_name: string | null
  article_title: string | null
}

export interface OperationLog {
  id: number
  user_id: number
  action: string
  target_type: string
  target_id: number | null
  detail: string | null
  created_at: string
}

export interface Stats {
  total_users: number
  total_articles: number
  total_comments: number
  total_categories: number
  total_tags: number
  published_articles: number
  draft_articles: number
  active_users: number
  today_new_users: number
  today_new_articles: number
  today_new_comments: number
}

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}
