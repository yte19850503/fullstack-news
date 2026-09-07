<template>
  <header class="site-header">
    <div class="header-inner">
      <router-link to="/" class="logo">AI 资讯站</router-link>

      <nav class="nav-categories">
        <router-link to="/" class="nav-link" :class="{ active: !activeCategory }">全部</router-link>
        <router-link
          v-for="cat in categories"
          :key="cat.id"
          :to="{ path: '/', query: { category_id: cat.id } }"
          class="nav-link"
          :class="{ active: activeCategory === cat.id }"
        >{{ cat.name }}</router-link>
      </nav>

      <div class="header-right">
        <form class="search-box" @submit.prevent="onSearch">
          <input v-model="searchQuery" type="text" placeholder="搜索文章..." />
          <button type="submit">搜索</button>
        </form>

        <template v-if="auth.isLoggedIn">
          <span class="user-name">{{ auth.user?.name }}</span>
          <button class="btn-logout" @click="auth.logout()">退出</button>
        </template>
        <router-link v-else to="/login" class="btn-login">登录</router-link>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const appStore = useAppStore()

const searchQuery = ref('')
const categories = computed(() => appStore.categories)
const activeCategory = computed(() => route.query.category_id ? Number(route.query.category_id) : null)

function onSearch() {
  const q = searchQuery.value.trim()
  if (q) router.push({ path: '/search', query: { q } })
}
</script>

<style scoped>
.site-header {
  background: var(--color-bg-white);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
  height: var(--header-height);
}

.header-inner {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 16px;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-primary);
  white-space: nowrap;
}

.nav-categories {
  display: flex;
  gap: 4px;
  overflow-x: auto;
  flex: 1;
}

.nav-link {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  color: var(--color-text-secondary);
  white-space: nowrap;
  transition: all 0.2s;
}

.nav-link:hover,
.nav-link.active {
  background: var(--color-primary);
  color: #fff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.search-box {
  display: flex;
  border: 1px solid var(--color-border);
  border-radius: 20px;
  overflow: hidden;
}

.search-box input {
  border: none;
  outline: none;
  padding: 6px 12px;
  font-size: 13px;
  width: 160px;
}

.search-box button {
  border: none;
  background: var(--color-primary);
  color: #fff;
  padding: 6px 14px;
  font-size: 13px;
  cursor: pointer;
}

.user-name {
  font-size: 14px;
  color: var(--color-text);
}

.btn-login,
.btn-logout {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  background: transparent;
}

.btn-login:hover,
.btn-logout:hover {
  background: var(--color-primary);
  color: #fff;
}
</style>
