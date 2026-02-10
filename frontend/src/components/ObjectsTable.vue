<template>
  <section class="table-container">
    <header class="table-header">
      <div class="header-title">
        <List :size="20" />
        <h2>Catalog</h2>
      </div>
      <div class="header-meta">
        <span class="result-count">{{ total.toLocaleString() }} total results</span>
      </div>
    </header>
    
    <div class="table-wrapper" v-if="objects.length">
      <table class="data-table">
        <thead>
          <tr>
            <th @click="handleSort('name')" :class="{ 'sortable': true, 'sorted': sortKey === 'name' }">
              <div class="th-content">
                <Star :size="14" />
                <span>Name</span>
                <component :is="getSortIcon('name')" :size="14" class="sort-icon" />
              </div>
            </th>
            <th @click="handleSort('constellation')" :class="{ 'sortable': true, 'sorted': sortKey === 'constellation' }">
              <div class="th-content">
                <Compass :size="14" />
                <span>Constellation</span>
                <component :is="getSortIcon('constellation')" :size="14" class="sort-icon" />
              </div>
            </th>
            <th @click="handleSort('magnitude')" :class="{ 'sortable': true, 'sorted': sortKey === 'magnitude' }">
              <div class="th-content">
                <Sparkles :size="14" />
                <span>Magnitude</span>
                <component :is="getSortIcon('magnitude')" :size="14" class="sort-icon" />
              </div>
            </th>
            <th @click="handleSort('distance_ly')" :class="{ 'sortable': true, 'sorted': sortKey === 'distance_ly' }">
              <div class="th-content">
                <Move :size="14" />
                <span>Distance (ly)</span>
                <component :is="getSortIcon('distance_ly')" :size="14" class="sort-icon" />
              </div>
            </th>
            <th @click="handleSort('spectral_type')" :class="{ 'sortable': true, 'sorted': sortKey === 'spectral_type' }">
              <div class="th-content">
                <Flame :size="14" />
                <span>Spectral Type</span>
                <component :is="getSortIcon('spectral_type')" :size="14" class="sort-icon" />
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="obj in sortedObjects" :key="obj.id" class="data-row">
            <td class="cell-name">{{ obj.name }}</td>
            <td>{{ obj.constellation }}</td>
            <td class="cell-numeric">{{ obj.magnitude.toFixed(2) }}</td>
            <td class="cell-numeric">{{ obj.distance_ly.toFixed(1) }}</td>
            <td>
              <span class="spectral-badge">{{ obj.spectral_type }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-else class="no-results">
      <Database :size="48" />
      <h3>No objects found</h3>
      <p>Try adjusting your filters to see more results</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from "pinia";
import { List, Star, Compass, Sparkles, Move, Flame, Database, ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-vue-next';
import { useCatalogStore } from "../stores/catalog";
import type { AstronomicalObject } from "../types";

const catalog = useCatalogStore();
const { objects, total } = storeToRefs(catalog);

type SortKey = 'name' | 'constellation' | 'magnitude' | 'distance_ly' | 'spectral_type';
type SortDirection = 'asc' | 'desc' | null;

const sortKey = ref<SortKey | null>(null);
const sortDirection = ref<SortDirection>(null);

const sortedObjects = computed(() => {
  if (!sortKey.value || !sortDirection.value) {
    return objects.value;
  }

  return [...objects.value].sort((a, b) => {
    const key = sortKey.value as SortKey;
    let aVal = a[key];
    let bVal = b[key];

    // Handle string comparison case-insensitively
    if (typeof aVal === 'string' && typeof bVal === 'string') {
      aVal = aVal.toLowerCase();
      bVal = bVal.toLowerCase();
    }

    if (aVal < bVal) return sortDirection.value === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortDirection.value === 'asc' ? 1 : -1;
    return 0;
  });
});

function handleSort(key: SortKey) {
  if (sortKey.value === key) {
    // Cycle through: asc -> desc -> null
    if (sortDirection.value === 'asc') {
      sortDirection.value = 'desc';
    } else if (sortDirection.value === 'desc') {
      sortDirection.value = null;
      sortKey.value = null;
    }
  } else {
    sortKey.value = key;
    sortDirection.value = 'asc';
  }
}

function getSortIcon(key: SortKey) {
  if (sortKey.value !== key) return ArrowUpDown;
  return sortDirection.value === 'asc' ? ArrowUp : ArrowDown;
}
</script>

<style scoped>
.table-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  overflow: hidden;
  margin-top: 1.5rem;
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--border);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-primary);
}

.header-title h2 {
  font-size: 1.125rem;
  font-weight: 600;
}

.result-count {
  font-size: 0.875rem;
  color: var(--text-tertiary);
  font-weight: 500;
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9375rem;
}

thead {
  background: var(--bg-elevated);
  position: sticky;
  top: 0;
  z-index: 10;
}

.th-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: space-between;
  width: 100%;
}

th {
  padding: 1rem 1.5rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.8125rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-tertiary);
  border-bottom: 1px solid var(--border);
}

th.sortable {
  cursor: pointer;
  user-select: none;
  transition: all 0.2s;
}

th.sortable:hover {
  background: var(--surface-hover);
  color: var(--text-secondary);
}

th.sorted {
  color: var(--primary);
  background: var(--primary-light);
}

.sort-icon {
  opacity: 0.3;
  transition: opacity 0.2s;
  flex-shrink: 0;
}

th.sortable:hover .sort-icon {
  opacity: 0.6;
}

th.sorted .sort-icon {
  opacity: 1;
  color: var(--primary);
}

.data-row {
  transition: background 0.15s;
  border-bottom: 1px solid var(--border);
}

.data-row:last-child {
  border-bottom: none;
}

.data-row:hover {
  background: var(--bg-elevated);
}

td {
  padding: 1rem 1.5rem;
  color: var(--text-secondary);
}

.cell-name {
  font-weight: 600;
  color: var(--text-primary);
}

.cell-numeric {
  font-feature-settings: 'tnum';
  font-variant-numeric: tabular-nums;
}

.spectral-badge {
  display: inline-block;
  padding: 0.25rem 0.625rem;
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  border-radius: 0.375rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--primary);
  font-family: monospace;
}

.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: var(--text-tertiary);
  text-align: center;
}

.no-results h3 {
  margin: 1rem 0 0.5rem;
  color: var(--text-secondary);
  font-size: 1.25rem;
}

.no-results p {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-tertiary);
}

@media (max-width: 768px) {
  th, td {
    padding: 0.75rem 1rem;
  }
}
</style>
