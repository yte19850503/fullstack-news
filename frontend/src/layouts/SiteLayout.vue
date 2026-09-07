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
  margin: 20px auto;
  padding: 0 16px;
}
</style>
