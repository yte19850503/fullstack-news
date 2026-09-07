<template>
  <div class="login-page">
    <div class="login-card">
      <h2 class="login-title">{{ isRegister ? '注册账号' : '登录' }}</h2>

      <form class="login-form" @submit.prevent="onSubmit">
        <div v-if="isRegister" class="form-group">
          <label>昵称</label>
          <input v-model="name" type="text" placeholder="请输入昵称" required />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="email" type="email" placeholder="请输入邮箱" required />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请输入密码" required />
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button type="submit" class="btn-submit" :disabled="submitting">
          {{ submitting ? '处理中...' : (isRegister ? '注册' : '登录') }}
        </button>
      </form>

      <p class="toggle-text">
        {{ isRegister ? '已有账号？' : '没有账号？' }}
        <a href="#" @click.prevent="isRegister = !isRegister">
          {{ isRegister ? '去登录' : '去注册' }}
        </a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const isRegister = ref(false)
const email = ref('')
const password = ref('')
const name = ref('')
const error = ref('')
const submitting = ref(false)

async function onSubmit() {
  error.value = ''
  submitting.value = true
  try {
    if (isRegister.value) {
      if (!name.value.trim()) {
        error.value = '请输入昵称'
        return
      }
      await auth.register(email.value, password.value, name.value)
    } else {
      await auth.login(email.value, password.value)
    }
    router.push('/')
  } catch (e: any) {
    error.value = e?.response?.data?.detail || '操作失败，请重试'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
}

.login-card {
  width: 400px;
  background: var(--color-bg-white);
  border-radius: var(--radius);
  padding: 40px 32px;
  box-shadow: var(--shadow);
}

.login-title {
  text-align: center;
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 28px;
  color: var(--color-text);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.form-group input {
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: var(--color-primary);
}

.error-msg {
  color: var(--color-danger);
  font-size: 13px;
  text-align: center;
}

.btn-submit {
  padding: 12px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 15px;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-text {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: var(--color-text-muted);
}

.toggle-text a {
  color: var(--color-primary);
  font-weight: 500;
}

@media (max-width: 480px) {
  .login-card {
    width: 90%;
    padding: 32px 20px;
  }
}
</style>
