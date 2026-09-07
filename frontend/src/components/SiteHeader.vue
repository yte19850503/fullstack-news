<template>
  <header class="site-header">
    <div class="header-container">
      <!-- Logo区域 -->
      <router-link to="/" class="logo">
        <span class="logo-icon">🤖</span>
        <span class="logo-text">AI Hub</span>
      </router-link>

      <!-- 桌面端分类导航 -->
      <nav class="nav-categories desktop-nav">
        <router-link to="/" class="nav-link" :class="{ active: !activeCategory }">全部</router-link>
        <router-link
          v-for="cat in categories.slice(0, 5)"
          :key="cat.id"
          :to="{ path: '/', query: { category_id: cat.id } }"
          class="nav-link"
          :class="{ active: activeCategory === cat.id }"
        >{{ cat.name }}</router-link>
      </nav>

      <!-- 右侧操作区 -->
      <div class="header-actions">
        <!-- 搜索框 - 桌面端 -->
        <form class="search-box desktop-search" @submit.prevent="onSearch">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="搜索文章..." 
            @focus="isSearchFocused = true"
            @blur="isSearchFocused = false"
          />
          <button type="submit" v-if="isSearchFocused || searchQuery">搜索</button>
        </form>

        <!-- 移动端搜索按钮 -->
        <button class="mobile-search-btn" @click="showMobileSearch = !showMobileSearch">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </button>

        <!-- 用户区域 -->
        <div class="user-section">
          <template v-if="auth.isLoggedIn">
            <div class="user-menu-trigger" @click="showUserMenu = !showUserMenu">
              <div class="user-avatar">{{ auth.user?.name?.[0]?.toUpperCase() || 'U' }}</div>
              <span class="user-name desktop-only">{{ auth.user?.name }}</span>
            </div>
            <div v-if="showUserMenu" class="user-dropdown">
              <router-link to="/profile" class="dropdown-item">个人中心</router-link>
              <button class="dropdown-item" @click="handleLogout">退出登录</button>
            </div>
          </template>
          <router-link v-else to="/login" class="btn-login">登录</router-link>
        </div>

        <!-- 移动端菜单按钮 -->
        <button class="mobile-menu-btn" @click="showMobileMenu = !showMobileMenu">
          <svg v-if="!showMobileMenu" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 移动端搜索面板 -->
    <div v-if="showMobileSearch" class="mobile-search-panel">
      <form @submit.prevent="onMobileSearch">
        <input 
          v-model="mobileSearchQuery" 
          type="text" 
          placeholder="搜索文章..."
          autofocus
        />
        <button type="submit">搜索</button>
      </form>
    </div>

    <!-- 移动端菜单面板 -->
    <div v-if="showMobileMenu" class="mobile-menu-panel">
      <nav class="mobile-nav-categories">
        <router-link 
          to="/" 
          class="mobile-nav-link" 
          :class="{ active: !activeCategory }"
          @click="closeMobileMenu"
        >
          全部
        </router-link>
        <router-link
          v-for="cat in categories"
          :key="cat.id"
          :to="{ path: '/', query: { category_id: cat.id } }"
          class="mobile-nav-link"
          :class="{ active: activeCategory === cat.id }"
          @click="closeMobileMenu"
        >
          {{ cat.name }}
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const appStore = useAppStore()

const searchQuery = ref('')
const mobileSearchQuery = ref('')
const isSearchFocused = ref(false)
const showMobileSearch = ref(false)
const showMobileMenu = ref(false)
const showUserMenu = ref(false)

const categories = computed(() => appStore.categories)
const activeCategory = computed(() => route.query.category_id ? Number(route.query.category_id) : null)

function onSearch() {
  const q = searchQuery.value.trim()
  if (q) {
    router.push({ path: '/search', query: { q } })
    searchQuery.value = ''
  }
}

function onMobileSearch() {
  const q = mobileSearchQuery.value.trim()
  if (q) {
    router.push({ path: '/search', query: { q } })
    mobileSearchQuery.value = ''
    showMobileSearch.value = false
  }
}

function handleLogout() {
  auth.logout()
  showUserMenu.value = false
}

function closeMobileMenu() {
  showMobileMenu.value = false
}

// 点击外部关闭下拉菜单
function handleClickOutside(event: MouseEvent) {
  const target = event.target as HTMLElement
  if (!target.closest('.user-section')) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.site-header {
  background: var(--color-bg-card);
  border-bottom: 1px solid var(--color-border-light);
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition);
}

.site-header:hover {
  box-shadow: var(--shadow);
}

.header-container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 var(--space-6);
  height: var(--header-height);
  display: flex;
  align-items: center;
  gap: var(--space-8);
}

/* Logo样式 */
.logo {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-xl);
  font-weight: 700;
  background: var(--color-primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  white-space: nowrap;
  transition: transform var(--transition-fast);
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: var(--text-2xl);
  filter: drop-shadow(0 2px 4px rgba(99, 102, 241, 0.3));
}

/* 桌面端导航 */
.desktop-nav {
  display: flex;
  gap: var(--space-2);
  overflow-x: auto;
  flex: 1;
  scrollbar-width: none;
}

.desktop-nav::-webkit-scrollbar {
  display: none;
}

.nav-link {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  white-space: nowrap;
  transition: all var(--transition-fast);
  position: relative;
}

.nav-link:hover {
  color: var(--color-primary);
  background: rgba(99, 102, 241, 0.08);
}

.nav-link.active {
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
  box-shadow: var(--shadow-sm);
}

/* 右侧操作区 */
.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  flex-shrink: 0;
}

/* 搜索框 */
.desktop-search {
  position: relative;
  display: flex;
  align-items: center;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-full);
  overflow: hidden;
  transition: all var(--transition);
  background: var(--color-bg);
}

.desktop-search:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  background: var(--color-bg-card);
}

.search-icon {
  width: 18px;
  height: 18px;
  margin-left: var(--space-3);
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.desktop-search input {
  border: none;
  outline: none;
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  width: 180px;
  background: transparent;
  color: var(--color-text);
  transition: width var(--transition);
}

.desktop-search input:focus {
  width: 220px;
}

.desktop-search button {
  border: none;
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  transition: opacity var(--transition-fast);
  margin-right: var(--space-1);
}

.desktop-search button:hover {
  opacity: 0.9;
}

/* 移动端搜索按钮 */
.mobile-search-btn {
  display: none;
  width: 40px;
  height: 40px;
  border-radius: var(--radius);
  background: var(--color-bg);
  color: var(--color-text-secondary);
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.mobile-search-btn svg {
  width: 20px;
  height: 20px;
}

.mobile-search-btn:hover {
  background: var(--color-primary);
  color: var(--color-text-inverse);
}

/* 用户区域 */
.user-section {
  position: relative;
}

.user-menu-trigger {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2);
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.user-menu-trigger:hover {
  background: var(--color-bg);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: var(--text-sm);
  box-shadow: var(--shadow-sm);
}

.user-name {
  font-size: var(--text-sm);
  color: var(--color-text);
  font-weight: 500;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  background: var(--color-bg-card);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  min-width: 160px;
  overflow: hidden;
  animation: slideDown 0.2s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-size: var(--text-sm);
  color: var(--color-text);
  background: none;
  border: none;
  cursor: pointer;
  transition: background var(--transition-fast);
}

.dropdown-item:hover {
  background: var(--color-bg);
  color: var(--color-primary);
}

.btn-login {
  padding: var(--space-2) var(--space-5);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: 500;
  border: 2px solid var(--color-primary);
  color: var(--color-primary);
  background: transparent;
  transition: all var(--transition-fast);
}

.btn-login:hover {
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
  border-color: transparent;
  box-shadow: var(--shadow-md);
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
  width: 40px;
  height: 40px;
  border-radius: var(--radius);
  background: var(--color-bg);
  color: var(--color-text-secondary);
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.mobile-menu-btn svg {
  width: 24px;
  height: 24px;
}

.mobile-menu-btn:hover {
  background: var(--color-primary);
  color: var(--color-text-inverse);
}

/* 移动端搜索面板 */
.mobile-search-panel {
  display: none;
  padding: var(--space-4) var(--space-6);
  background: var(--color-bg-card);
  border-top: 1px solid var(--color-border-light);
  animation: slideDown 0.2s ease;
}

.mobile-search-panel form {
  display: flex;
  gap: var(--space-2);
}

.mobile-search-panel input {
  flex: 1;
  padding: var(--space-3) var(--space-4);
  border: 2px solid var(--color-border);
  border-radius: var(--radius);
  font-size: var(--text-base);
  transition: border-color var(--transition-fast);
}

.mobile-search-panel input:focus {
  border-color: var(--color-primary);
}

.mobile-search-panel button {
  padding: var(--space-3) var(--space-6);
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
  border-radius: var(--radius);
  font-size: var(--text-sm);
  font-weight: 500;
  transition: opacity var(--transition-fast);
}

.mobile-search-panel button:hover {
  opacity: 0.9;
}

/* 移动端菜单面板 */
.mobile-menu-panel {
  display: none;
  padding: var(--space-4) var(--space-6);
  background: var(--color-bg-card);
  border-top: 1px solid var(--color-border-light);
  animation: slideDown 0.2s ease;
}

.mobile-nav-categories {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.mobile-nav-link {
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius);
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
}

.mobile-nav-link:hover {
  background: var(--color-bg);
  color: var(--color-primary);
}

.mobile-nav-link.active {
  background: var(--color-primary-gradient);
  color: var(--color-text-inverse);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .header-container {
    gap: var(--space-4);
  }
  
  .desktop-nav {
    gap: var(--space-1);
  }
  
  .nav-link {
    padding: var(--space-2) var(--space-3);
    font-size: var(--text-xs);
  }
  
  .desktop-search input {
    width: 140px;
  }
  
  .desktop-search input:focus {
    width: 160px;
  }
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 var(--space-4);
  }
  
  .logo-text {
    font-size: var(--text-lg);
  }
  
  .desktop-nav,
  .desktop-search,
  .desktop-only {
    display: none;
  }
  
  .mobile-search-btn,
  .mobile-menu-btn {
    display: flex;
  }
  
  .mobile-search-panel,
  .mobile-menu-panel {
    display: block;
  }
  
  .user-name {
    display: none;
  }
}

@media (max-width: 480px) {
  :root {
    --header-height: 60px;
  }
  
  .header-container {
    padding: 0 var(--space-3);
    gap: var(--space-2);
  }
  
  .logo-icon {
    font-size: var(--text-xl);
  }
  
  .logo-text {
    font-size: var(--text-base);
  }
  
  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: var(--text-xs);
  }
}
</style>
