<template>
  <div class="status-bar">
    <span v-if="loading">Loading latest data…</span>
    <span v-else-if="error" class="error">{{ error }}</span>
    <span v-else>
      Filters active · magnitude {{ filters.magnitude_min ?? "—" }} – {{ filters.magnitude_max ?? "—" }} ·
      {{ total }} objects
    </span>
    <button @click="catalog.refresh()">Refresh (Ctrl/Cmd + R)</button>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useCatalogStore } from "../stores/catalog";

const catalog = useCatalogStore();
const { loading, error, filters, total } = storeToRefs(catalog);
</script>

<style scoped>
.status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  border-radius: 999px;
  border: 1px solid var(--accent-muted);
  background: rgba(15, 23, 42, 0.9);
  margin-bottom: 1rem;
}
button {
  border: none;
  background: transparent;
  color: var(--accent);
  cursor: pointer;
}
.error {
  color: #f87171;
}
</style>
