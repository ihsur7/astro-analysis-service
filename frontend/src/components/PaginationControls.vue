<template>
  <div class="pagination">
    <button @click="goFirst" :disabled="isFirst" class="pagination-btn">
      <ChevronsLeft :size="16" />
      <span class="btn-text">First</span>
    </button>
    <button @click="goPrev" :disabled="isFirst" class="pagination-btn">
      <ChevronLeft :size="16" />
      <span>Previous</span>
    </button>
    
    <div class="page-info">
      <span class="page-label">Page</span>
      <span class="page-current">{{ filters.page }}</span>
      <span class="page-separator">of</span>
      <span class="page-total">{{ maxPages }}</span>
    </div>
    
    <button @click="goNext" :disabled="isLast" class="pagination-btn">
      <span>Next</span>
      <ChevronRight :size="16" />
    </button>
    <button @click="goLast" :disabled="isLast" class="pagination-btn">
      <span class="btn-text">Last</span>
      <ChevronsRight :size="16" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-vue-next';
import { useCatalogStore } from "../stores/catalog";

const catalog = useCatalogStore();
const { filters, pages } = storeToRefs(catalog);

const maxPages = computed(() => Math.max(1, pages.value || 1));
const isFirst = computed(() => filters.value.page <= 1);
const isLast = computed(() => filters.value.page >= maxPages.value);

function goFirst() {
  if (isFirst.value) return;
  catalog.setFilters({ page: 1 });
  catalog.refresh();
}

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

function goLast() {
  if (isLast.value) return;
  catalog.setFilters({ page: maxPages.value });
  catalog.refresh();
}
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.625rem 1rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: var(--surface-hover);
  border-color: var(--primary);
  color: var(--primary);
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1rem;
  font-size: 0.9375rem;
}

.page-label, .page-separator {
  color: var(--text-tertiary);
}

.page-current {
  font-weight: 700;
  font-size: 1.125rem;
  color: var(--primary);
}

.page-total {
  font-weight: 600;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .btn-text {
    display: none;
  }
  
  .pagination-btn {
    padding: 0.625rem;
  }
}
</style>
