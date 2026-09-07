<template>
  <div>
    <el-card>
      <div class="filter-bar">
        <el-select v-model="query.status" placeholder="文章状态" clearable style="width: 140px">
          <el-option label="草稿" value="DRAFT" />
          <el-option label="已发布" value="PUBLISHED" />
          <el-option label="已归档" value="ARCHIVED" />
        </el-select>
        <el-input v-model="query.q" placeholder="搜索标题" clearable style="width: 200px" />
        <el-button type="primary" @click="loadData">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
        <el-button type="success" @click="router.push('/articles/new')">新增文章</el-button>
      </div>

      <div v-if="selection.length > 0" class="batch-bar">
        <span>已选 {{ selection.length }} 项</span>
        <el-select v-model="batchStatus" placeholder="批量操作" style="width: 120px; margin-left: 12px">
          <el-option label="发布" value="PUBLISHED" />
          <el-option label="草稿" value="DRAFT" />
          <el-option label="归档" value="ARCHIVED" />
        </el-select>
        <el-button type="warning" size="small" @click="handleBatch" :disabled="!batchStatus">批量更新</el-button>
      </div>

      <el-table :data="tableData" v-loading="loading" @selection-change="onSelectionChange" stripe>
        <el-table-column type="selection" width="50" />
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="标题" show-overflow-tooltip />
        <el-table-column prop="author_name" label="作者" width="120" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="view_count" label="浏览" width="80" />
        <el-table-column prop="created_at" label="发布时间" width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="360" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="router.push(`/articles/${row.id}`)">查看</el-button>
            <el-button type="primary" size="small" @click="router.push(`/articles/${row.id}/edit`)">编辑</el-button>
            <el-popconfirm title="确定删除此文章？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
            <el-button
              v-if="row.status !== 'PUBLISHED'"
              type="success"
              size="small"
              @click="handleReview(row.id, 'PUBLISHED')"
            >发布</el-button>
            <el-button
              v-if="row.status !== 'DRAFT'"
              type="warning"
              size="small"
              @click="handleReview(row.id, 'DRAFT')"
            >转草稿</el-button>
            <el-button
              v-if="row.status !== 'ARCHIVED'"
              type="info"
              size="small"
              @click="handleReview(row.id, 'ARCHIVED')"
            >归档</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="query.page"
        v-model:page-size="query.page_size"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        style="margin-top: 16px; justify-content: flex-end"
        @size-change="loadData"
        @current-change="loadData"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { listArticles, reviewArticle, batchUpdateArticles, deleteArticle } from '@/api/article'
import { formatDate } from '@/utils/format'
import type { AdminArticle, ArticleStatus } from '@/types'

const router = useRouter()

const loading = ref(false)
const tableData = ref<AdminArticle[]>([])
const total = ref(0)
const selection = ref<AdminArticle[]>([])
const batchStatus = ref<ArticleStatus | ''>('')

const query = reactive({
  page: 1,
  page_size: 20,
  status: '',
  q: '',
})

function statusType(s: string) {
  return s === 'PUBLISHED' ? 'success' : s === 'DRAFT' ? 'warning' : 'info'
}

function statusLabel(s: string) {
  return s === 'PUBLISHED' ? '已发布' : s === 'DRAFT' ? '草稿' : '已归档'
}

function onSelectionChange(rows: AdminArticle[]) {
  selection.value = rows
}

async function loadData() {
  loading.value = true
  try {
    const params: Record<string, any> = { page: query.page, page_size: query.page_size }
    if (query.status) params.status = query.status
    if (query.q) params.q = query.q
    const res = await listArticles(params)
    tableData.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function resetQuery() {
  query.status = ''
  query.q = ''
  query.page = 1
  loadData()
}

async function handleReview(id: number, status: ArticleStatus) {
  await reviewArticle(id, status)
  ElMessage.success('操作成功')
  loadData()
}

async function handleDelete(id: number) {
  await deleteArticle(id)
  ElMessage.success('文章已删除')
  loadData()
}

async function handleBatch() {
  if (!batchStatus.value || selection.value.length === 0) return
  const ids = selection.value.map((a) => a.id)
  await batchUpdateArticles(ids, batchStatus.value as ArticleStatus)
  ElMessage.success(`已批量更新 ${ids.length} 篇文章`)
  batchStatus.value = ''
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.batch-bar {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: #ecf5ff;
  border-radius: 4px;
  font-size: 14px;
}
</style>
