<template>
  <div>
    <el-card>
      <div class="header-bar">
        <h3 style="margin: 0">用户管理</h3>
        <div>
          <el-select v-model="role" placeholder="角色筛选" clearable style="width: 140px; margin-right: 12px" @change="handleSearch">
            <el-option label="ADMIN" value="ADMIN" />
            <el-option label="EDITOR" value="EDITOR" />
            <el-option label="READER" value="READER" />
          </el-select>
          <el-input
            v-model="keyword"
            placeholder="搜索邮箱 / 昵称"
            clearable
            style="width: 200px; margin-right: 12px"
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          />
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </div>
      </div>

      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="name" label="昵称" width="140" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'ADMIN' ? 'danger' : row.role === 'EDITOR' ? 'warning' : 'info'" size="small">
              {{ row.role }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-switch
              :model-value="row.is_active"
              @change="(val: boolean) => handleToggle(row, val)"
            />
          </template>
        </el-table-column>
        <el-table-column label="注册时间" width="170">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="90" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openDialog(row)">编辑</el-button>
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

    <el-dialog v-model="dialogVisible" title="编辑用户" width="480px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="昵称" prop="name">
          <el-input v-model="form.name" placeholder="用户昵称" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" style="width: 100%">
            <el-option label="ADMIN" value="ADMIN" />
            <el-option label="EDITOR" value="EDITOR" />
            <el-option label="READER" value="READER" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { listUsers, updateUser, toggleUserActive } from '@/api/user'
import { formatDate } from '@/utils/format'
import type { AdminUser } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const tableData = ref<AdminUser[]>([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const role = ref('')
const keyword = ref('')

const dialogVisible = ref(false)
const editId = ref(0)
const formRef = ref<FormInstance>()
const form = reactive({ name: '', role: '' })

const rules: FormRules = {
  name: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
}

async function loadData() {
  loading.value = true
  try {
    const params: { page: number; page_size: number; role?: string; q?: string } = {
      page: page.value,
      page_size: pageSize.value,
    }
    if (role.value) params.role = role.value
    if (keyword.value) params.q = keyword.value
    const res = await listUsers(params)
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

function openDialog(row: AdminUser) {
  editId.value = row.id
  form.name = row.name
  form.role = row.role
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await updateUser(editId.value, { name: form.name, role: form.role })
    ElMessage.success('更新成功')
    dialogVisible.value = false
    loadData()
  } finally {
    submitting.value = false
  }
}

async function handleToggle(row: AdminUser, val: boolean) {
  await toggleUserActive(row.id, val)
  ElMessage.success(val ? '已启用' : '已禁用')
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
