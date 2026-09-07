<template>
  <div class="search-page">
    <div class="search-header">
      <h2>搜索结果：{{ query }}</h2>
      <span class="result-count" v-if="total > 0">共 {{ total }} 篇</span>
    </div>

    <div class="article-list">
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>搜索中...</p>
      </div>
      <template v-else>
        <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
        <p v-if="!articles.length" class="empty-state">未找到相关文章</p>
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
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { searchArticles } from '@/api/article'
import { useSeo } from '@/composables/useSeo'
import type { ArticleBrief } from '@/types'
import ArticleCard from '@/components/ArticleCard.vue'
import Pagination from '@/components/Pagination.vue'

const route = useRoute()
const articles = ref<ArticleBrief[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const query = ref('')

useSeo(() => ({
  title: query.value ? `"${query.value}" 的搜索结果 - AI 资讯站` : '搜索 - AI 资讯站',
  description: query.value ? `搜索"${query.value}"的结果，共 ${total.value} 篇相关文章` : '在 AI 资讯站搜索文章',
}))

async function doSearch() {
  const q = route.query.q as string
  if (!q) return
  query.value = q
  loading.value = true
  try {
    const res = await searchArticles(q, page.value, pageSize)
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
  doSearch()
}

watch(
  () => route.query.q,
  () => {
    page.value = 1
    doSearch()
  },
  { immediate: true }
)
</script>

<style scoped>
.search-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
}

.search-header {
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
  margin-bottom: var(--space-6);
  padding: var(--space-6);
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

.search-header h2 {
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--color-text);
}

.result-count {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.article-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}

.loading-state,
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: var(--space-12) 0;
  color: var(--color-text-muted);
  font-size: var(--text-base);
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

/* 平板端响应式 */
@media (max-width: 1024px) {
  .article-list {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-5);
  }
}

/* 移动端响应式 */
@media (max-width: 768px) {
  .search-page {
    padding: 0 var(--space-4);
  }
  
  .search-header {
    padding: var(--space-5);
  }
  
  .search-header h2 {
    font-size: var(--text-lg);
  }
  
  .article-list {
    grid-template-columns: 1fr;
    gap: var(--space-5);
  }
}

/* 小屏幕手机优化 */
@media (max-width: 480px) {
  .search-page {
    padding: 0 var(--space-3);
  }
  
  .search-header {
    padding: var(--space-4);
  }
  
  .search-header h2 {
    font-size: var(--text-base);
  }
  
  .loading-state,
  .empty-state {
    padding: var(--space-8) 0;
    font-size: var(--text-sm);
  }
}
</style>
