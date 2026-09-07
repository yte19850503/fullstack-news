<template>
  <div>
    <el-page-header @back="router.back()">
      <template #content>
        <span>{{ isEdit ? '编辑文章' : '新增文章' }}</span>
      </template>
    </el-page-header>

    <el-card style="margin-top: 16px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文章标题" @input="onTitleChange" />
        </el-form-item>

        <el-form-item label="Slug">
          <el-input v-model="form.slug" placeholder="自动生成，可手动修改" />
        </el-form-item>

        <el-form-item label="分类" prop="category_id">
          <el-select v-model="form.category_id" placeholder="请选择分类" style="width: 100%">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="标签">
          <el-select v-model="form.tag_ids" multiple placeholder="请选择标签" style="width: 100%">
            <el-option v-for="t in tags" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="摘要">
          <el-input v-model="form.summary" type="textarea" :rows="3" placeholder="文章摘要（选填）" />
        </el-form-item>

        <el-form-item label="封面图">
          <el-input v-model="form.cover_image" placeholder="封面图 URL（选填）" />
        </el-form-item>

        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio value="DRAFT">草稿</el-radio>
            <el-radio value="PUBLISHED">发布</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="正文" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="20" placeholder="请输入文章正文（支持 HTML）" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSubmit" :loading="submitting">
            {{ isEdit ? '保存修改' : '创建文章' }}
          </el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import {
  getArticle, createArticle, updateArticle,
  getCategories, getTags,
  type ArticleFormData, type ArticleDetail,
} from '@/api/article'
import type { Category, Tag } from '@/types'

const router = useRouter()
const route = useRoute()
const formRef = ref<FormInstance>()
const submitting = ref(false)

const isEdit = computed(() => !!route.params.id)

const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])

const form = reactive<ArticleFormData & { slug: string }>({
  title: '',
  slug: '',
  content: '',
  summary: '',
  cover_image: '',
  category_id: 0,
  tag_ids: [],
  status: 'DRAFT',
})

const rules: FormRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  content: [{ required: true, message: '请输入正文', trigger: 'blur' }],
}

function onTitleChange(val: string) {
  if (!isEdit.value && !form.slug) {
    form.slug = val
      .toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
      .replace(/^-|-$/g, '')
  }
}

async function loadData() {
  const [cats, tg] = await Promise.all([getCategories(), getTags()])
  categories.value = cats
  tags.value = tg

  if (isEdit.value) {
    const id = Number(route.params.id)
    const article = await getArticle(id)
    form.title = article.title
    form.slug = article.slug
    form.content = article.content
    form.summary = article.summary || ''
    form.cover_image = article.cover_image || ''
    form.category_id = article.category?.id || 0
    form.tag_ids = article.tags?.map((t) => t.id) || []
    form.status = article.status
  }
}

async function onSubmit() {
  await formRef.value?.validate()
  submitting.value = true
  try {
    const data: ArticleFormData = {
      title: form.title,
      content: form.content,
      summary: form.summary || undefined,
      cover_image: form.cover_image || undefined,
      category_id: form.category_id,
      tag_ids: form.tag_ids?.length ? form.tag_ids : undefined,
      status: form.status,
    }

    if (isEdit.value) {
      await updateArticle(Number(route.params.id), data)
      ElMessage.success('文章已更新')
    } else {
      await createArticle(data)
      ElMessage.success('文章已创建')
    }
    router.push('/articles')
  } finally {
    submitting.value = false
  }
}

onMounted(loadData)
</script>
