<template>
  <div class="pagination" v-if="totalPages > 1">
    <button :disabled="current <= 1" @click="$emit('change', current - 1)">上一页</button>
    <template v-for="p in visiblePages" :key="p">
      <span v-if="p === '...'" class="ellipsis">...</span>
      <button v-else :class="{ active: p === current }" @click="$emit('change', p as number)">{{ p }}</button>
    </template>
    <button :disabled="current >= totalPages" @click="$emit('change', current + 1)">下一页</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  current: number
  total: number
  pageSize: number
}>()

defineEmits<{ change: [page: number] }>()

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  const tp = totalPages.value
  const c = props.current

  if (tp <= 7) {
    for (let i = 1; i <= tp; i++) pages.push(i)
    return pages
  }

  pages.push(1)
  if (c > 3) pages.push('...')
  for (let i = Math.max(2, c - 1); i <= Math.min(tp - 1, c + 1); i++) {
    pages.push(i)
  }
  if (c < tp - 2) pages.push('...')
  pages.push(tp)

  return pages
})
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  gap: 4px;
  margin-top: 24px;
}

.pagination button {
  padding: 6px 12px;
  border: 1px solid var(--color-border);
  background: var(--color-bg-white);
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  color: var(--color-text);
  transition: all 0.2s;
}

.pagination button:hover:not(:disabled) {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.pagination button.active {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.ellipsis {
  padding: 6px 8px;
  color: var(--color-text-muted);
}
</style>
