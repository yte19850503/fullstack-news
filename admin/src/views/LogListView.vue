<template>
  <div>
    <el-card>
      <div class="header-bar">
        <h3 style="margin: 0">操作日志</h3>
        <el-select v-model="action" placeholder="操作类型筛选" clearable style="width: 200px" @change="handleSearch">
          <el-option v-for="a in actionOptions" :key="a" :label="a" :value="a" />
        </el-select>
      </div>

      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="user_id" label="用户 ID" width="90" />
        <el-table-column prop="action" label="操作" width="140" />
        <el-table-column prop="target_type" label="目标类型" width="120" />
        <el-table-column prop="target_id" label="目标 ID" width="90" />
        <el-table-column prop="detail" label="详情" show-overflow-tooltip />
        <el-table-column label="时间" width="170">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
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
import { listLogs } from '@/api/log'
import { formatDate } from '@/utils/format'
import type { OperationLog } from '@/types'

const loading = ref(false)
const tableData = ref<OperationLog[]>([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const action = ref('')

const actionOptions = [
  'CREATE_TAG', 'UPDATE_TAG', 'DELETE_TAG',
  'CREATE_CATEGORY', 'UPDATE_CATEGORY', 'DELETE_CATEGORY',
  'UPDATE_USER', 'TOGGLE_USER_ACTIVE',
  'REVIEW_ARTICLE', 'BATCH_UPDATE_ARTICLES',
  'DELETE_COMMENT',
]

async function loadData() {
  loading.value = true
  try {
    const params: { page: number; page_size: number; action?: string } = {
      page: page.value,
      page_size: pageSize.value,
    }
    if (action.value) params.action = action.value
    const res = await listLogs(params)
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
