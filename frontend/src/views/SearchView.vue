<template>
  <div class="search-page">
    <div class="search-header">
      <h2>搜索结果：{{ query }}</h2>
      <span class="result-count" v-if="total > 0">共 {{ total }} 篇</span>
    </div>

    <div class="article-list">
      <div v-if="loading" class="loading">搜索中...</div>
      <template v-else>
        <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
        <p v-if="!articles.length" class="empty">未找到相关文章</p>
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
  max-width: 800px;
  margin: 0 auto;
}

.search-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 20px;
}

.search-header h2 {
  font-size: 20px;
  font-weight: 600;
}

.result-count {
  font-size: 14px;
  color: var(--color-text-muted);
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
}
</style>
