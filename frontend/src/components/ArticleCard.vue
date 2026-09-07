<template>
  <router-link :to="`/article/${article.slug}`" class="article-card">
    <div v-if="article.cover_image" class="card-cover">
      <img :src="article.cover_image" :alt="article.title" loading="lazy" />
    </div>
    <div class="card-body">
      <h3 class="card-title">{{ article.title }}</h3>
      <p v-if="article.summary" class="card-summary">{{ article.summary }}</p>
      <div class="card-meta">
        <span v-if="article.author" class="meta-author">{{ article.author.name }}</span>
        <span v-if="article.category" class="meta-category">{{ article.category.name }}</span>
        <span class="meta-time">{{ formatDate(article.created_at) }}</span>
        <span class="meta-views">{{ article.view_count }} 阅读</span>
      </div>
      <div v-if="article.tags?.length" class="card-tags">
        <span v-for="tag in article.tags.slice(0, 3)" :key="tag.id" class="tag">{{ tag.name }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import type { ArticleBrief } from '@/types'

defineProps<{ article: ArticleBrief }>()

function formatDate(iso: string) {
  if (!iso) return ''
  const d = new Date(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}
</script>

<style scoped>
.article-card {
  display: flex;
  background: var(--color-bg-white);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: box-shadow 0.2s;
  text-decoration: none;
  color: inherit;
}

.article-card:hover {
  box-shadow: var(--shadow-hover);
}

.card-cover {
  width: 200px;
  min-height: 140px;
  flex-shrink: 0;
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-body {
  flex: 1;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--color-text);
}

.card-summary {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: var(--color-text-muted);
}

.card-tags {
  display: flex;
  gap: 6px;
}

.tag {
  padding: 2px 8px;
  background: #e6f7ff;
  color: var(--color-primary);
  border-radius: 10px;
  font-size: 12px;
}

@media (max-width: 640px) {
  .article-card {
    flex-direction: column;
  }
  .card-cover {
    width: 100%;
    height: 180px;
  }
}
</style>
