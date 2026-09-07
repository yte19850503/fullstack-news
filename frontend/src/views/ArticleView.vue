<template>
  <div class="article-page">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="!article" class="error">
      <p>文章不存在或已被删除</p>
      <router-link to="/">返回首页</router-link>
    </div>
    <template v-else>
      <article class="article-content">
        <h1 class="article-title">{{ article.title }}</h1>

        <div class="article-meta">
          <span v-if="article.author" class="meta-author">{{ article.author.name }}</span>
          <span v-if="article.category" class="meta-category">{{ article.category.name }}</span>
          <span class="meta-time">{{ formatDateTime(article.created_at) }}</span>
          <span class="meta-views">{{ article.view_count }} 阅读</span>
        </div>

        <div v-if="article.cover_image" class="article-cover">
          <img :src="article.cover_image" :alt="article.title" loading="lazy" />
        </div>

        <div class="article-body" v-html="article.content"></div>

        <div v-if="article.tags?.length" class="article-tags">
          <span v-for="tag in article.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
        </div>
      </article>

      <AdSlot position="inarticle" />

      <CommentSection :article-id="article.id" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getArticle } from '@/api/article'
import { useSeo } from '@/composables/useSeo'
import type { ArticleDetail } from '@/types'
import AdSlot from '@/components/AdSlot.vue'
import CommentSection from '@/components/CommentSection.vue'

const route = useRoute()
const article = ref<ArticleDetail | null>(null)
const loading = ref(true)

useSeo(() => {
  if (!article.value) return {}
  const a = article.value
  const tags = a.tags?.map(t => t.name).join(',') ?? ''
  return {
    title: `${a.title} - AI 资讯站`,
    description: a.summary || a.title,
    keywords: tags || a.category?.name || '',
    ogTitle: a.title,
    ogDescription: a.summary || a.title,
    ogImage: a.cover_image || '',
    ogType: 'article',
    ogUrl: `${window.location.origin}/article/${route.params.slug}`,
    jsonLd: {
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: a.title,
      description: a.summary || a.title,
      image: a.cover_image || '',
      datePublished: a.created_at || '',
      author: { '@type': 'Person', name: a.author?.name || '' },
      publisher: { '@type': 'Organization', name: 'AI 资讯站' },
    },
  }
})

function formatDateTime(iso: string) {
  if (!iso) return ''
  const d = new Date(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

async function loadArticle(slug: string) {
  loading.value = true
  try {
    article.value = await getArticle(slug)
  } catch (e) {
    console.error('Failed to load article:', e)
    article.value = null
  } finally {
    loading.value = false
  }
}

watch(
  () => route.params.slug,
  (slug) => {
    if (slug) loadArticle(slug as string)
  },
  { immediate: true }
)
</script>

<style scoped>
.article-page {
  max-width: 800px;
  margin: 0 auto;
}

.loading,
.error {
  text-align: center;
  padding: 60px 0;
  color: var(--color-text-muted);
}

.error a {
  margin-top: 12px;
  display: inline-block;
}

.article-content {
  background: var(--color-bg-white);
  border-radius: var(--radius);
  padding: 32px;
  box-shadow: var(--shadow);
}

.article-title {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: 16px;
  color: var(--color-text);
}

.article-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: var(--color-text-muted);
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.article-cover {
  margin-bottom: 24px;
  border-radius: var(--radius);
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  display: block;
}

.article-body {
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-text);
}

.article-body :deep(p) {
  margin-bottom: 16px;
}

.article-body :deep(h2) {
  font-size: 22px;
  margin: 24px 0 12px;
}

.article-body :deep(h3) {
  font-size: 18px;
  margin: 20px 0 10px;
}

.article-body :deep(img) {
  border-radius: var(--radius);
  margin: 16px 0;
}

.article-body :deep(pre) {
  background: #f6f8fa;
  padding: 16px;
  border-radius: var(--radius);
  overflow-x: auto;
  font-size: 14px;
  margin: 16px 0;
}

.article-body :deep(code) {
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 14px;
}

.article-body :deep(pre code) {
  background: none;
  padding: 0;
}

.article-tags {
  display: flex;
  gap: 8px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.tag {
  padding: 4px 12px;
  background: #e6f7ff;
  color: var(--color-primary);
  border-radius: 14px;
  font-size: 13px;
}

@media (max-width: 640px) {
  .article-content {
    padding: 20px 16px;
  }
  .article-title {
    font-size: 22px;
  }
}
</style>
