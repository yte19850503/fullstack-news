<template>
  <div class="site-layout">
    <SiteHeader />
    <div class="site-container">
      <router-view />
    </div>
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import SiteHeader from '@/components/SiteHeader.vue'
import SiteFooter from '@/components/SiteFooter.vue'
</script>

<style scoped>
.site-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.site-container {
  flex: 1;
  max-width: var(--max-width);
  width: 100%;
  margin: 0 auto;
  padding: var(--space-6);
}

/* 平板端响应式 */
@media (max-width: 1024px) {
  .site-container {
    padding: var(--space-5);
  }
}

/* 移动端响应式 */
@media (max-width: 768px) {
  .site-container {
    padding: var(--space-4);
  }
}

/* 小屏幕手机优化 */
@media (max-width: 480px) {
  .site-container {
    padding: var(--space-3);
  }
}
</style>
