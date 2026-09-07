<template>
  <div class="article-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="!article" class="error-state">
      <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p>文章不存在或已被删除</p>
      <router-link to="/" class="back-link">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        返回首页
      </router-link>
    </div>
    
    <!-- 文章内容 -->
    <template v-else>
      <article class="article-content">
        <!-- 文章头部 -->
        <header class="article-header">
          <h1 class="article-title">{{ article.title }}</h1>
          
          <div class="article-meta">
            <div class="meta-left">
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
            </div>
            <div class="meta-right">
              <span class="meta-item meta-time">
                <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                {{ formatDateTime(article.created_at) }}
              </span>
              <span class="meta-item meta-views">
                <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                {{ article.view_count }}
              </span>
            </div>
          </div>
        </header>

        <!-- 封面图 -->
        <div v-if="article.cover_image" class="article-cover">
          <img 
            :src="article.cover_image" 
            :alt="article.title" 
            loading="lazy"
          />
        </div>

        <!-- 文章正文 -->
        <div class="article-body" v-html="article.content"></div>

        <!-- 标签 -->
        <div v-if="article.tags?.length" class="article-tags">
          <span class="tags-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
            </svg>
            标签：
          </span>
          <span v-for="tag in article.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
        </div>
      </article>

      <!-- 文中广告 -->
      <AdSlot position="inarticle" />

      <!-- 评论区 -->
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
  max-width: var(--content-max-width);
  margin: 0 auto;
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: var(--space-12) 0;
  color: var(--color-text-muted);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto var(--space-4);
  border: 4px solid var(--color-border);
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

/* 错误状态 */
.error-state {
  text-align: center;
  padding: var(--space-12) 0;
  color: var(--color-text-muted);
}

.error-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--space-4);
  color: var(--color-text-muted);
  opacity: 0.5;
}

.error-state p {
  font-size: var(--text-base);
  margin-bottom: var(--space-4);
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: 500;
  transition: all var(--transition-fast);
}

.back-link svg {
  width: 18px;
  height: 18px;
}

.back-link:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 文章内容卡片 */
.article-content {
  background: var(--color-bg-card);
  border-radius: var(--radius-xl);
  padding: var(--space-10);
  box-shadow: var(--shadow-lg);
  margin-bottom: var(--space-8);
}

/* 文章头部 */
.article-header {
  margin-bottom: var(--space-8);
}

.article-title {
  font-size: var(--text-3xl);
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: var(--space-5);
  color: var(--color-text);
  letter-spacing: -0.02em;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);
  flex-wrap: wrap;
}

.meta-left,
.meta-right {
  display: flex;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.meta-icon {
  width: 16px;
  height: 16px;
  color: var(--color-text-muted);
}

/* 封面图 */
.article-cover {
  margin-bottom: var(--space-8);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow);
}

.article-cover img {
  width: 100%;
  display: block;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

/* 文章正文 */
.article-body {
  font-size: var(--text-lg);
  line-height: 1.8;
  color: var(--color-text);
}

.article-body :deep(p) {
  margin-bottom: var(--space-5);
}

.article-body :deep(h2) {
  font-size: var(--text-2xl);
  font-weight: 600;
  margin: var(--space-8) 0 var(--space-4);
  color: var(--color-text);
  padding-bottom: var(--space-2);
  border-bottom: 2px solid var(--color-border-light);
}

.article-body :deep(h3) {
  font-size: var(--text-xl);
  font-weight: 600;
  margin: var(--space-6) 0 var(--space-3);
  color: var(--color-text);
}

.article-body :deep(img) {
  border-radius: var(--radius);
  margin: var(--space-6) 0;
  box-shadow: var(--shadow);
  max-width: 100%;
}

.article-body :deep(pre) {
  background: #f8fafc;
  padding: var(--space-5);
  border-radius: var(--radius);
  overflow-x: auto;
  font-size: var(--text-sm);
  margin: var(--space-5) 0;
  border: 1px solid var(--color-border-light);
}

.article-body :deep(code) {
  background: rgba(99, 102, 241, 0.1);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-size: 0.9em;
  color: var(--color-primary-dark);
}

.article-body :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.article-body :deep(blockquote) {
  border-left: 4px solid var(--color-primary);
  padding-left: var(--space-5);
  margin: var(--space-5) 0;
  color: var(--color-text-secondary);
  font-style: italic;
  background: rgba(99, 102, 241, 0.05);
  padding: var(--space-4) var(--space-5);
  border-radius: 0 var(--radius) var(--radius) 0;
}

.article-body :deep(ul),
.article-body :deep(ol) {
  margin: var(--space-5) 0;
  padding-left: var(--space-6);
}

.article-body :deep(li) {
  margin-bottom: var(--space-2);
}

.article-body :deep(a) {
  color: var(--color-primary);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.article-body :deep(a:hover) {
  color: var(--color-primary-dark);
}

/* 标签区域 */
.article-tags {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-top: var(--space-8);
  padding-top: var(--space-6);
  border-top: 1px solid var(--color-border-light);
  flex-wrap: wrap;
}

.tags-label {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  font-weight: 500;
}

.tags-label svg {
  width: 16px;
  height: 16px;
}

.tag {
  padding: var(--space-2) var(--space-4);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
  color: var(--color-primary);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: 500;
  transition: all var(--transition-fast);
}

.tag:hover {
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

/* 平板端响应式 */
@media (max-width: 1024px) {
  .article-content {
    padding: var(--space-8);
  }
  
  .article-title {
    font-size: var(--text-2xl);
  }
  
  .article-body {
    font-size: var(--text-base);
  }
}

/* 移动端响应式 */
@media (max-width: 768px) {
  .article-page {
    padding: 0 var(--space-4);
  }
  
  .article-content {
    padding: var(--space-6);
    border-radius: var(--radius-lg);
  }
  
  .article-title {
    font-size: var(--text-xl);
    margin-bottom: var(--space-4);
  }
  
  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-3);
  }
  
  .meta-left,
  .meta-right {
    width: 100%;
  }
  
  .article-body {
    font-size: var(--text-base);
    line-height: 1.7;
  }
  
  .article-body :deep(h2) {
    font-size: var(--text-xl);
  }
  
  .article-body :deep(h3) {
    font-size: var(--text-lg);
  }
  
  .article-cover {
    margin-bottom: var(--space-6);
  }
}

/* 小屏幕手机优化 */
@media (max-width: 480px) {
  .article-page {
    padding: 0 var(--space-3);
  }
  
  .article-content {
    padding: var(--space-5);
  }
  
  .article-title {
    font-size: var(--text-lg);
  }
  
  .meta-item {
    font-size: var(--text-xs);
  }
  
  .article-body {
    font-size: 15px;
  }
  
  .tag {
    font-size: var(--text-xs);
    padding: var(--space-1) var(--space-3);
  }
}
</style>
