<template>
  <section class="panel">
    <header>
      <h2>Filters</h2>
      <button class="ghost" @click="handleReset">Reset</button>
    </header>
    <p class="hint">Lower magnitude = brighter object.</p>
    <form @submit.prevent="handleApply" class="filters-grid">
      <label>
        <span>Magnitude min</span>
        <input v-model.number="form.magnitude_min" type="number" step="0.01" placeholder="--" />
      </label>
      <label>
        <span>Magnitude max</span>
        <input v-model.number="form.magnitude_max" type="number" step="0.01" placeholder="--" />
      </label>
      <label>
        <span>Distance min (ly)</span>
        <input v-model.number="form.distance_min" type="number" step="1" placeholder="--" />
      </label>
      <label>
        <span>Distance max (ly)</span>
        <input v-model.number="form.distance_max" type="number" step="1" placeholder="--" />
      </label>
      <label>
        <span>Constellation</span>
        <input v-model="form.constellation" type="text" placeholder="Orion" />
      </label>
      <label>
        <span>Spectral type</span>
        <input v-model="form.spectral_type" type="text" placeholder="G2" />
      </label>
      <label class="col-span-2">
        <span>Search (name or constellation)</span>
        <input v-model="form.search" type="text" placeholder="Rigel" />
      </label>
      <label>
        <span>Rows per page</span>
        <input v-model.number="form.page_size" type="number" min="1" max="100" />
      </label>
      <button type="submit">Apply</button>
    </form>
  </section>
</template>

<script setup lang="ts">
import { reactive, watch } from "vue";
import { storeToRefs } from "pinia";
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
.panel {
  background: var(--panel);
  border: 1px solid var(--accent-muted);
  border-radius: 16px;
  padding: 1.5rem;
  flex: 1 1 320px;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
button {
  border: 1px solid var(--accent);
  background: transparent;
  color: var(--accent);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
button.ghost {
  border: none;
  color: var(--muted);
}
.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.85rem;
}
input {
  padding: 0.65rem;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.4);
  border-radius: 8px;
  color: var(--text);
}
.col-span-2 {
  grid-column: span 2;
}
.hint {
  color: var(--muted);
  margin-top: 0.25rem;
}
</style>
