<template>
  <div class="home">
    <div class="home-main">
      <div class="article-list">
        <div v-if="loading" class="loading">加载中...</div>
        <template v-else>
          <template v-for="(article, index) in articles" :key="article.id">
            <ArticleCard :article="article" />
            <AdSlot v-if="(index + 1) % 5 === 0" position="infeed" />
          </template>
          <p v-if="!articles.length" class="empty">暂无文章</p>
        </template>
      </div>
      <Pagination
        v-if="total > 0"
        :current="page"
        :total="total"
        :page-size="pageSize"
        @change="onPageChange"
      />
    </div>

    <aside class="home-sidebar">
      <AdSlot position="sidebar" />
      <div class="sidebar-section">
        <h3 class="sidebar-title">热门标签</h3>
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
  title: '首页 - AI 资讯站',
  description: 'AI 资讯站 — 聚焦 AI 工具、短剧资讯的科技新闻平台，每日更新最新行业动态',
  keywords: 'AI,人工智能,科技新闻,AI工具,短剧',
  ogTitle: 'AI 资讯站',
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
  display: flex;
  gap: 24px;
}

.home-main {
  flex: 1;
  min-width: 0;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.loading,
.empty {
  text-align: center;
  padding: 40px 0;
  color: var(--color-text-muted);
  font-size: 15px;
}

.home-sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
}

.sidebar-section {
  background: var(--color-bg-white);
  border-radius: var(--radius);
  padding: 16px;
  margin-top: 16px;
  box-shadow: var(--shadow);
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--color-text);
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-link {
  padding: 4px 12px;
  background: #f0f0f0;
  border-radius: 14px;
  font-size: 13px;
  color: var(--color-text-secondary);
  transition: all 0.2s;
}

.tag-link:hover,
.tag-link.active {
  background: var(--color-primary);
  color: #fff;
}

@media (max-width: 768px) {
  .home {
    flex-direction: column;
  }
  .home-sidebar {
    width: 100%;
  }
}
</style>
