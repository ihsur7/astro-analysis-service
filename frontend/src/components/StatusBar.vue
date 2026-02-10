<template>
  <div class="status-bar">
    <div class="status-content">
      <div v-if="loading" class="status-item loading">
        <Loader2 :size="16" class="spin" />
        <span>Loading data...</span>
      </div>
      <div v-else-if="error" class="status-item error">
        <AlertCircle :size="16" />
        <span>{{ error }}</span>
      </div>
      <div v-else class="status-item success">
        <CheckCircle2 :size="16" />
        <span>{{ total.toLocaleString() }} objects loaded</span>
      </div>
      
      <div class="status-filters">
        <span class="filter-item" v-if="filters.magnitude_min || filters.magnitude_max">
          <Sparkles :size="14" />
          Mag: {{ filters.magnitude_min ?? '—' }} - {{ filters.magnitude_max ?? '—' }}
        </span>
        <span class="filter-item" v-if="filters.distance_min || filters.distance_max">
          <Ruler :size="14" />
          Dist: {{ filters.distance_min ?? '—' }} - {{ filters.distance_max ?? '—' }} ly
        </span>
        <span class="filter-item" v-if="filters.constellation">
          <Star :size="14" />
          {{ filters.constellation }}
        </span>
        <span class="filter-item" v-if="filters.search">
          <Search :size="14" />
          "{{ filters.search }}"
        </span>
      </div>
    </div>
    
    <button @click="catalog.refresh()" class="refresh-btn" :disabled="loading">
      <RefreshCw :size="16" :class="{ spin: loading }" />
      <span>Refresh</span>
      <kbd>Ctrl+R</kbd>
    </button>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { Loader2, AlertCircle, CheckCircle2, RefreshCw, Sparkles, Ruler, Star, Search } from 'lucide-vue-next';
import { useCatalogStore } from "../stores/catalog";

const catalog = useCatalogStore();
const { loading, error, filters, total } = storeToRefs(catalog);
</script>

<style scoped>
.status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
}

.status-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  flex: 1;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9375rem;
  font-weight: 500;
}

.status-item.loading {
  color: var(--primary);
}

.status-item.error {
  color: var(--error);
}

.status-item.success {
  color: var(--success);
}

.status-filters {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  border-radius: 0.375rem;
  font-size: 0.8125rem;
  color: var(--text-secondary);
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.refresh-btn:hover:not(:disabled) {
  background: var(--surface-hover);
  border-color: var(--primary);
  color: var(--primary);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

kbd {
  padding: 0.125rem 0.375rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-family: monospace;
  color: var(--text-tertiary);
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .status-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .refresh-btn {
    justify-content: center;
  }
  
  kbd {
    display: none;
  }
}
</style>
