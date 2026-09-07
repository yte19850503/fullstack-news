<template>
  <div>
    <el-card>
      <div class="header-bar">
        <h3 style="margin: 0">评论管理</h3>
        <div>
          <el-input
            v-model="articleId"
            placeholder="按文章 ID 筛选"
            clearable
            style="width: 180px; margin-right: 12px"
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          />
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </div>
      </div>

      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="article_title" label="所属文章" show-overflow-tooltip />
        <el-table-column prop="user_name" label="评论用户" width="120" />
        <el-table-column prop="content" label="内容" show-overflow-tooltip />
        <el-table-column label="创建时间" width="170">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="90" fixed="right">
          <template #default="{ row }">
            <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-bar">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="loadData"
          @current-change="loadData"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listComments, deleteComment } from '@/api/comment'
import { formatDate } from '@/utils/format'
import type { AdminComment } from '@/types'

const loading = ref(false)
const tableData = ref<AdminComment[]>([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const articleId = ref('')

async function loadData() {
  loading.value = true
  try {
    const params: { page: number; page_size: number; article_id?: number } = {
      page: page.value,
      page_size: pageSize.value,
    }
    if (articleId.value) {
      const id = Number(articleId.value)
      if (!isNaN(id)) params.article_id = id
    }
    const res = await listComments(params)
    tableData.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  loadData()
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('确定删除该评论？', '提示', { type: 'warning' })
  await deleteComment(id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.pagination-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
