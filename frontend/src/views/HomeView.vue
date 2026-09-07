<template>
  <div class="home">
    <div class="home-main">
      <!-- 文章列表 - 响应式网格 -->
      <div class="article-grid">
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
        <template v-else>
          <template v-for="(article, index) in articles" :key="article.id">
            <ArticleCard :article="article" class="grid-item" />
            <AdSlot v-if="(index + 1) % 5 === 0" position="infeed" class="ad-infeed" />
          </template>
          <p v-if="!articles.length" class="empty-state">暂无文章</p>
        </template>
      </div>
      
      <!-- 分页 -->
      <Pagination
        v-if="total > 0"
        :current="page"
        :total="total"
        :page-size="pageSize"
        @change="onPageChange"
      />
    </div>

    <!-- 侧边栏 -->
    <aside class="home-sidebar">
      <AdSlot position="sidebar" />
      <div class="sidebar-section">
        <h3 class="sidebar-title">
          <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"/>
          </svg>
          热门标签
        </h3>
        <div class="tag-cloud">
          <router-link
            v-for="tag in tags"
            :key="tag.id"
            :to="{ path: '/', query: { tag_id: tag.id } }"
            class="tag-link"
            :class="{ active: activeTag === tag.id }"
          >{{ tag.name }}</router-link>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticles } from '@/api/article'
import { useAppStore } from '@/stores/app'
import { useSeo } from '@/composables/useSeo'
import type { ArticleBrief } from '@/types'
import ArticleCard from '@/components/ArticleCard.vue'
import Pagination from '@/components/Pagination.vue'
import AdSlot from '@/components/AdSlot.vue'

useSeo({
  title: '首页 - FullStack News',
  description: 'FullStack News — 聚焦 AI 工具、短剧资讯的科技新闻平台，每日更新最新行业动态',
  keywords: 'AI,人工智能,科技新闻,AI工具,短剧',
  ogTitle: 'FullStack News',
  ogDescription: '聚焦 AI 工具、短剧资讯的科技新闻平台',
  ogType: 'website',
})

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()

const articles = ref<ArticleBrief[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)

const activeCategory = ref<number | null>(null)
const activeTag = ref<number | null>(null)

async function loadArticles() {
  loading.value = true
  try {
    const params: Record<string, any> = {
      page: page.value,
      page_size: pageSize,
      status: 'PUBLISHED',
      sort: 'newest',
    }
    if (activeCategory.value) params.category_id = activeCategory.value
    if (activeTag.value) params.tag_id = activeTag.value
    const res = await getArticles(params)
    articles.value = res.items
    total.value = res.total
  } catch {
    articles.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function onPageChange(p: number) {
  page.value = p
  window.scrollTo({ top: 0, behavior: 'smooth' })
  loadArticles()
}

watch(
  () => route.query,
  (q) => {
    activeCategory.value = q.category_id ? Number(q.category_id) : null
    activeTag.value = q.tag_id ? Number(q.tag_id) : null
    page.value = 1
    loadArticles()
  },
  { immediate: false }
)

onMounted(() => {
  appStore.loadBaseData()
  activeCategory.value = route.query.category_id ? Number(route.query.category_id) : null
  activeTag.value = route.query.tag_id ? Number(route.query.tag_id) : null
  loadArticles()
})

const tags = appStore.tags
</script>

<style scoped>
.home {
  display: grid;
  grid-template-columns: 1fr var(--sidebar-width);
  gap: var(--space-8);
  align-items: start;
}

.home-main {
  min-width: 0;
}

/* 响应式文章网格 */
.article-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}

.ad-infeed {
  grid-column: 1 / -1;
}

/* 加载状态 */
.loading-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: var(--space-12) 0;
  color: var(--color-text-muted);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto var(--space-4);
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  font-size: var(--text-sm);
}

/* 空状态 */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: var(--space-12) 0;
  color: var(--color-text-muted);
  font-size: var(--text-base);
}

/* 侧边栏 */
.home-sidebar {
  position: sticky;
  top: calc(var(--header-height) + var(--space-6));
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.sidebar-section {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow);
  transition: box-shadow var(--transition);
}

.sidebar-section:hover {
  box-shadow: var(--shadow-md);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-lg);
  font-weight: 600;
  margin-bottom: var(--space-4);
  color: var(--color-text);
}

.title-icon {
  width: 20px;
  height: 20px;
  color: var(--color-primary);
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.tag-link {
  padding: var(--space-2) var(--space-3);
  background: var(--color-bg);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  border: 1px solid transparent;
}

.tag-link:hover {
  background: rgba(99, 102, 241, 0.1);
  color: var(--color-primary);
  border-color: var(--color-primary-light);
  transform: translateY(-2px);
}

.tag-link.active {
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
  box-shadow: var(--shadow-sm);
}

/* 平板端响应式 */
@media (max-width: 1024px) {
  .home {
    grid-template-columns: 1fr 280px;
    gap: var(--space-6);
  }
  
  .article-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-5);
  }
}

/* 移动端响应式 - 单列布局 */
@media (max-width: 768px) {
  .home {
    grid-template-columns: 1fr;
    gap: var(--space-6);
  }
  
  .article-grid {
    grid-template-columns: 1fr;
    gap: var(--space-5);
  }
  
  .home-sidebar {
    position: static;
    order: 2;
  }
  
  .sidebar-section {
    padding: var(--space-5);
  }
}

/* 小屏幕手机优化 */
@media (max-width: 480px) {
  :root {
    --space-6: 16px;
  }
  
  .article-grid {
    gap: var(--space-4);
  }
  
  .loading-state,
  .empty-state {
    padding: var(--space-8) 0;
  }
}
</style>
