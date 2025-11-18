<template>
  <div class="pagination">
    <button :disabled="isFirst" @click="goPrev">Prev</button>
    <span>Page {{ filters.page }} / {{ maxPages }}</span>
    <button :disabled="isLast" @click="goNext">Next</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useCatalogStore } from "../stores/catalog";

const catalog = useCatalogStore();
const { filters, pages } = storeToRefs(catalog);

const maxPages = computed(() => Math.max(1, pages.value || 1));
const isFirst = computed(() => filters.value.page <= 1);
const isLast = computed(() => filters.value.page >= maxPages.value);

function goPrev() {
  if (isFirst.value) return;
  catalog.setFilters({ page: filters.value.page - 1 });
  catalog.refresh();
}

function goNext() {
  if (isLast.value) return;
  catalog.setFilters({ page: filters.value.page + 1 });
  catalog.refresh();
}
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
button {
  border: 1px solid var(--accent);
  background: transparent;
  color: var(--accent);
  padding: 0.4rem 0.9rem;
  border-radius: 8px;
  cursor: pointer;
}
button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
span {
  color: var(--muted);
}
</style>
