<template>
  <section class="filters-panel">
    <header class="panel-header">
      <div class="header-title">
        <Filter :size="20" />
        <h2>Filters</h2>
      </div>
      <button class="btn-ghost" @click="handleReset">
        <RotateCcw :size="16" />
        <span>Reset</span>
      </button>
    </header>
    <p class="info-text">
      <Info :size="14" />
      Lower magnitude values indicate brighter objects
    </p>
    <form @submit.prevent="handleApply" class="filters-form">
      <div class="form-group">
        <label>
          <span class="label-text">Magnitude Min</span>
          <input v-model.number="form.magnitude_min" type="number" step="0.01" placeholder="e.g., 0" />
        </label>
        <label>
          <span class="label-text">Magnitude Max</span>
          <input v-model.number="form.magnitude_max" type="number" step="0.01" placeholder="e.g., 15" />
        </label>
      </div>
      
      <div class="form-group">
        <label>
          <span class="label-text">Distance Min (ly)</span>
          <input v-model.number="form.distance_min" type="number" step="1" placeholder="e.g., 0" />
        </label>
        <label>
          <span class="label-text">Distance Max (ly)</span>
          <input v-model.number="form.distance_max" type="number" step="1" placeholder="e.g., 1000" />
        </label>
      </div>
      
      <div class="form-group">
        <label>
          <span class="label-text">Constellation</span>
          <input v-model="form.constellation" type="text" placeholder="e.g., Orion" />
        </label>
        <label>
          <span class="label-text">Spectral Type</span>
          <input v-model="form.spectral_type" type="text" placeholder="e.g., G2" />
        </label>
      </div>
      
      <label class="full-width">
        <span class="label-text">Search</span>
        <div class="input-with-icon">
          <Search :size="16" class="input-icon" />
          <input v-model="form.search" type="text" placeholder="Search by name or constellation" class="with-icon" />
        </div>
      </label>
      
      <label class="full-width">
        <span class="label-text">Results Per Page</span>
        <input v-model.number="form.page_size" type="number" min="1" max="100" />
      </label>
      
      <button type="submit" class="btn-primary">
        <Play :size="16" />
        <span>Apply Filters</span>
      </button>
    </form>
  </section>
</template>

<script setup lang="ts">
import { reactive, watch } from "vue";
import { storeToRefs } from "pinia";
import { Filter, RotateCcw, Info, Search, Play } from 'lucide-vue-next';
import { useCatalogStore } from "../stores/catalog";

const catalog = useCatalogStore();
const { filters } = storeToRefs(catalog);

const form = reactive({ ...filters.value });

watch(
  filters,
  (next) => {
    Object.assign(form, next);
  },
  { deep: true }
);

function handleApply() {
  catalog.setFilters({ ...form, page: 1 });
  catalog.refresh();
}

function handleReset() {
  catalog.resetFilters();
}
</script>

<style scoped>
.filters-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
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

.btn-ghost {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  color: var(--text-tertiary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-ghost:hover {
  background: var(--surface-hover);
  border-color: var(--text-tertiary);
  color: var(--text-secondary);
}

.info-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  border-radius: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.8125rem;
  margin-bottom: 1.5rem;
}

.filters-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.full-width {
  grid-column: 1 / -1;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-text {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
}

input {
  padding: 0.75rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  color: var(--text-primary);
  font-size: 0.9375rem;
  transition: all 0.2s;
}

input:focus {
  outline: none;
  border-color: var(--border-focus);
  background: var(--surface);
}

input::placeholder {
  color: var(--text-muted);
}

.input-with-icon {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

input.with-icon {
  padding-left: 2.5rem;
}

.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: var(--primary);
  border: none;
  border-radius: 0.5rem;
  color: white;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.5rem;
}

.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(136, 136, 136, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}
</style>
