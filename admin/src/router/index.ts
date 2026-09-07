import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { title: '登录' },
    },
    {
      path: '/',
      component: () => import('@/layouts/AdminLayout.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('@/views/DashboardView.vue'),
          meta: { title: '仪表盘', icon: 'Odometer' },
        },
        {
          path: 'articles',
          name: 'articles',
          component: () => import('@/views/ArticleListView.vue'),
          meta: { title: '文章管理', icon: 'Document' },
        },
        {
          path: 'articles/new',
          name: 'article-new',
          component: () => import('@/views/ArticleFormView.vue'),
          meta: { title: '新增文章' },
        },
        {
          path: 'articles/:id/edit',
          name: 'article-edit',
          component: () => import('@/views/ArticleFormView.vue'),
          meta: { title: '编辑文章' },
        },
        {
          path: 'articles/:id',
          name: 'article-detail',
          component: () => import('@/views/ArticleDetailView.vue'),
          meta: { title: '文章详情' },
        },
        {
          path: 'categories',
          name: 'categories',
          component: () => import('@/views/CategoryListView.vue'),
          meta: { title: '分类管理', icon: 'Menu' },
        },
        {
          path: 'tags',
          name: 'tags',
          component: () => import('@/views/TagListView.vue'),
          meta: { title: '标签管理', icon: 'PriceTag' },
        },
        {
          path: 'comments',
          name: 'comments',
          component: () => import('@/views/CommentListView.vue'),
          meta: { title: '评论管理', icon: 'ChatDotRound' },
        },
        {
          path: 'users',
          name: 'users',
          component: () => import('@/views/UserListView.vue'),
          meta: { title: '用户管理', icon: 'User', requiresAdmin: true },
        },
        {
          path: 'logs',
          name: 'logs',
          component: () => import('@/views/LogListView.vue'),
          meta: { title: '操作日志', icon: 'Tickets', requiresAdmin: true },
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/dashboard',
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  document.title = `${to.meta.title ?? '页面'} - 新闻管理后台`

  if (to.path === '/login') {
    if (auth.isLoggedIn) return '/dashboard'
    return true
  }

  if (!auth.isLoggedIn) {
    return `/login?redirect=${encodeURIComponent(to.fullPath)}`
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    ElMessage.warning('需要管理员权限')
    return '/dashboard'
  }

  return true
})

export default router
