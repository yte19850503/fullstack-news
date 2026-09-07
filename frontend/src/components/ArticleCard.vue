<template>
  <router-link :to="`/article/${article.slug}`" class="article-card">
    <!-- 顶部封面图 -->
    <div class="card-cover">
      <img 
        :src="coverImage" 
        :alt="article.title" 
        loading="lazy"
      />
    </div>
    
    <!-- 底部内容区 -->
    <div class="card-body">
      <h3 class="card-title">{{ article.title }}</h3>
      <p v-if="article.summary" class="card-summary">{{ article.summary }}</p>
      
      <div class="card-meta">
        <span v-if="article.author" class="meta-item meta-author">
          <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          {{ article.author.name }}
        </span>
        <span v-if="article.category" class="meta-item meta-category">
          <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
          </svg>
          {{ article.category.name }}
        </span>
        <span class="meta-item meta-time">
          <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          {{ formatDate(article.created_at) }}
        </span>
        <span class="meta-item meta-views">
          <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
          </svg>
          {{ article.view_count }}
        </span>
      </div>
      
      <div v-if="article.tags?.length" class="card-tags">
        <span v-for="tag in article.tags.slice(0, 3)" :key="tag.id" class="tag">{{ tag.name }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ArticleBrief } from '@/types'
import { generateCoverSVG } from '@/utils/image'

const props = defineProps<{ article: ArticleBrief }>()

const coverImage = computed(() => {
  return props.article.cover_image || generateCoverSVG(
    props.article.title,
    props.article.category?.name
  )
})

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
  flex-direction: column;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: all var(--transition);
  text-decoration: none;
  color: inherit;
  position: relative;
}

.article-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(236, 72, 153, 0.05) 100%);
  opacity: 0;
  transition: opacity var(--transition);
  pointer-events: none;
  z-index: 0;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.article-card:hover::before {
  opacity: 1;
}

/* 封面图 - 2:1比例（比16:9更紧凑） */
.card-cover {
  width: 100%;
  aspect-ratio: 2 / 1;
  position: relative;
  overflow: hidden;
  background: var(--color-bg);
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.article-card:hover .card-cover img {
  transform: scale(1.05);
}

/* 内容区 */
.card-body {
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  position: relative;
  z-index: 1;
}

.card-title {
  font-size: var(--text-lg);
  font-weight: 600;
  line-height: 1.5;
  color: var(--color-text);
  margin: 0;
  transition: color var(--transition-fast);
}

.article-card:hover .card-title {
  color: var(--color-primary);
}

.card-summary {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: var(--space-4);
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.meta-icon {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.card-tags {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.tag {
  padding: var(--space-1) var(--space-3);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
  color: var(--color-primary);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 500;
  transition: all var(--transition-fast);
}

.tag:hover {
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
  transform: translateY(-2px);
}

/* 移动端优化 */
@media (max-width: 768px) {
  .card-cover {
    aspect-ratio: auto;
    height: 120px;
  }
  
  .card-body {
    padding: var(--space-4);
  }
  
  .card-title {
    font-size: var(--text-base);
  }
  
  .card-summary {
    font-size: var(--text-xs);
  }
  
  .card-meta {
    font-size: 11px;
    gap: var(--space-3);
  }
  
  .meta-icon {
    width: 12px;
    height: 12px;
  }
  
  .tag {
    font-size: 11px;
    padding: 2px var(--space-2);
  }
}
</style>
