<template>
  <div class="comment-section">
    <h3 class="section-title">评论 ({{ comments.length }})</h3>

    <form v-if="auth.isLoggedIn" class="comment-form" @submit.prevent="onSubmit">
      <textarea v-model="newComment" placeholder="写下你的评论..." rows="3" />
      <button type="submit" :disabled="!newComment.trim()">发表评论</button>
    </form>
    <p v-else class="login-hint">
      <router-link to="/login">登录</router-link> 后发表评论
    </p>

    <div class="comment-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="comment-author">{{ comment.user?.name ?? '匿名' }}</span>
          <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
        </div>
        <div class="comment-content">{{ comment.content }}</div>

        <button v-if="auth.isLoggedIn" class="reply-toggle" @click="toggleReply(comment.id)">
          回复
        </button>

        <form
          v-if="replyingTo === comment.id"
          class="comment-form reply-form"
          @submit.prevent="onReply(comment.id)"
        >
          <textarea v-model="replyContent" placeholder="回复..." rows="2" />
          <button type="submit" :disabled="!replyContent.trim()">回复</button>
        </form>

        <div v-if="comment.replies?.length" class="reply-list">
          <div v-for="reply in comment.replies" :key="reply.id" class="comment-item reply-item">
            <div class="comment-header">
              <span class="comment-author">{{ reply.user?.name ?? '匿名' }}</span>
              <span class="comment-time">{{ formatDate(reply.created_at) }}</span>
            </div>
            <div class="comment-content">{{ reply.content }}</div>
          </div>
        </div>
      </div>

      <p v-if="!comments.length" class="empty-hint">暂无评论</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getComments, postComment } from '@/api/comment'
import type { Comment } from '@/types'

const props = defineProps<{ articleId: number }>()
const auth = useAuthStore()

const comments = ref<Comment[]>([])
const newComment = ref('')
const replyingTo = ref<number | null>(null)
const replyContent = ref('')

function formatDate(iso: string) {
  if (!iso) return ''
  const d = new Date(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

async function loadComments() {
  try {
    comments.value = await getComments(props.articleId)
  } catch {
    comments.value = []
  }
}

async function onSubmit() {
  if (!newComment.value.trim()) return
  await postComment(props.articleId, newComment.value)
  newComment.value = ''
  await loadComments()
}

function toggleReply(commentId: number) {
  replyingTo.value = replyingTo.value === commentId ? null : commentId
  replyContent.value = ''
}

async function onReply(parentId: number) {
  if (!replyContent.value.trim()) return
  await postComment(props.articleId, replyContent.value, parentId)
  replyContent.value = ''
  replyingTo.value = null
  await loadComments()
}

loadComments()
</script>

<style scoped>
.comment-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border);
}

.section-title {
  font-size: 18px;
  margin-bottom: 16px;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.comment-form textarea {
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 10px;
  font-size: 14px;
  resize: vertical;
  font-family: inherit;
}

.comment-form button {
  align-self: flex-end;
  padding: 8px 20px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 14px;
}

.comment-form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-hint {
  color: var(--color-text-muted);
  font-size: 14px;
  margin-bottom: 16px;
}

.comment-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.comment-header {
  display: flex;
  gap: 12px;
  margin-bottom: 6px;
}

.comment-author {
  font-weight: 600;
  font-size: 14px;
}

.comment-time {
  font-size: 12px;
  color: var(--color-text-muted);
}

.comment-content {
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text);
}

.reply-toggle {
  background: none;
  border: none;
  color: var(--color-primary);
  font-size: 13px;
  cursor: pointer;
  margin-top: 4px;
  padding: 0;
}

.reply-form {
  margin-top: 8px;
  margin-left: 20px;
}

.reply-list {
  margin-left: 20px;
  padding-left: 12px;
  border-left: 2px solid #f0f0f0;
}

.reply-item {
  padding: 8px 0;
}

.empty-hint {
  color: var(--color-text-muted);
  font-size: 14px;
  text-align: center;
  padding: 20px 0;
}
</style>
