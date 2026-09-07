<template>
  <div>
    <el-page-header @back="router.back()">
      <template #content>
        <span>文章详情</span>
      </template>
      <template #extra>
        <el-button type="primary" @click="router.push(`/articles/${id}/edit`)">编辑</el-button>
        <el-popconfirm title="确定删除此文章？" @confirm="handleDelete">
          <template #reference>
            <el-button type="danger">删除</el-button>
          </template>
        </el-popconfirm>
      </template>
    </el-page-header>

    <el-card v-if="article" style="margin-top: 16px">
      <h2 style="margin: 0 0 16px">{{ article.title }}</h2>

      <el-descriptions :column="3" border>
        <el-descriptions-item label="作者">{{ article.author?.name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ article.category?.name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusType(article.status)">{{ statusLabel(article.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="浏览量">{{ article.view_count }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(article.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formatDate(article.updated_at) }}</el-descriptions-item>
        <el-descriptions-item label="Slug" :span="3">{{ article.slug }}</el-descriptions-item>
        <el-descriptions-item label="标签" :span="3">
          <el-tag v-for="t in article.tags" :key="t.id" style="margin-right: 6px" size="small">
            {{ t.name }}
          </el-tag>
          <span v-if="!article.tags?.length">-</span>
        </el-descriptions-item>
      </el-descriptions>

      <div v-if="article.cover_image" style="margin-top: 16px">
        <img :src="article.cover_image" alt="封面图" style="max-width: 100%; max-height: 400px; border-radius: 8px" />
      </div>

      <div v-if="article.summary" style="margin-top: 16px; padding: 12px; background: #f5f7fa; border-radius: 6px; color: #606266; font-size: 14px; line-height: 1.6">
        <strong>摘要：</strong>{{ article.summary }}
      </div>

      <div style="margin-top: 20px; line-height: 1.8; font-size: 15px" v-html="article.content" />
    </el-card>

    <el-skeleton v-else :rows="10" animated />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getArticle, deleteArticle, type ArticleDetail } from '@/api/article'
import { formatDate } from '@/utils/format'

const router = useRouter()
const route = useRoute()
const id = Number(route.params.id)
const article = ref<ArticleDetail | null>(null)

function statusType(s: string) {
  return s === 'PUBLISHED' ? 'success' : s === 'DRAFT' ? 'warning' : 'info'
}

function statusLabel(s: string) {
  return s === 'PUBLISHED' ? '已发布' : s === 'DRAFT' ? '草稿' : '已归档'
}

async function handleDelete() {
  await deleteArticle(id)
  ElMessage.success('文章已删除')
  router.push('/articles')
}

onMounted(async () => {
  article.value = await getArticle(id)
})
</script>
