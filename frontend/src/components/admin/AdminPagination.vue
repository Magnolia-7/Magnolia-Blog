<template>
  <nav v-if="totalPages > 1" class="admin-pagination" :aria-label="label">
    <button type="button" :disabled="page <= 1 || loading" @click="changePage(page - 1)">上一页</button>
    <button
      v-for="pageNumber in pageNumbers"
      :key="pageNumber"
      type="button"
      :class="{ active: pageNumber === page }"
      :aria-current="pageNumber === page ? 'page' : undefined"
      :disabled="loading"
      @click="changePage(pageNumber)"
    >{{ pageNumber }}</button>
    <button type="button" :disabled="page >= totalPages || loading" @click="changePage(page + 1)">下一页</button>
  </nav>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true },
  loading: Boolean,
  label: { type: String, default: "分页" },
});
const emit = defineEmits(["change"]);

const pageNumbers = computed(() => {
  const end = Math.min(props.totalPages, Math.max(5, props.page + 2));
  const start = Math.max(1, Math.min(props.page - 2, end - 4));
  return Array.from({ length: Math.max(0, end - start + 1) }, (_, index) => start + index);
});

function changePage(page) {
  if (props.loading || page < 1 || page > props.totalPages || page === props.page) return;
  emit("change", page);
}
</script>

<style scoped>
.admin-pagination { display: flex; justify-content: center; gap: 6px; }
.admin-pagination button { min-width: 36px; min-height: 36px; padding: 0 11px; border: 1px solid var(--line); border-radius: 9px; color: var(--muted-strong); background: #fff; }
.admin-pagination button.active { color: #fff; border-color: var(--rose-600); background: var(--rose-600); }
.admin-pagination button:disabled { cursor: not-allowed; opacity: .45; }
@media (max-width: 640px) { .admin-pagination { flex-wrap: wrap; } }
</style>
