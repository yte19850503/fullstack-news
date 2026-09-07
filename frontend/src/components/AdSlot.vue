<template>
  <div v-if="ads.length" class="ad-slot" :class="`ad-${position}`">
    <div
      v-for="ad in ads"
      :key="ad.id"
      class="ad-item"
      v-html="ad.code"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getPublicAds } from '@/api/ad'
import type { AdPublic } from '@/types'

const props = defineProps<{ position: string }>()
const ads = ref<AdPublic[]>([])

onMounted(async () => {
  try {
    ads.value = await getPublicAds(props.position)
  } catch {
    // silently ignore ad load failures
  }
})
</script>

<style scoped>
.ad-slot {
  margin: 16px 0;
}

.ad-item {
  overflow: hidden;
  border-radius: var(--radius);
}

.ad-item :deep(img) {
  max-width: 100%;
}
</style>
