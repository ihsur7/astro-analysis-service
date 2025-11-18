<template>
  <section class="panel table-panel">
    <header>
      <div>
        <h2>Catalog</h2>
        <small>{{ total }} total</small>
      </div>
    </header>
    <div class="table-wrapper" v-if="objects.length">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Constellation</th>
            <th>Magnitude</th>
            <th>Distance (ly)</th>
            <th>Spectral</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="obj in objects" :key="obj.id">
            <td>{{ obj.name }}</td>
            <td>{{ obj.constellation }}</td>
            <td>{{ obj.magnitude.toFixed(2) }}</td>
            <td>{{ obj.distance_ly.toFixed(1) }}</td>
            <td>{{ obj.spectral_type }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="placeholder">No objects match the active filters.</p>
  </section>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useCatalogStore } from "../stores/catalog";

const catalog = useCatalogStore();
const { objects, total } = storeToRefs(catalog);
</script>

<style scoped>
.table-panel {
  margin-top: 1.5rem;
  background: var(--panel);
  border: 1px solid var(--accent-muted);
  border-radius: 16px;
  padding: 1.5rem;
}
.table-wrapper {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}
th,
td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid rgba(148, 163, 184, 0.25);
}
th {
  color: var(--muted);
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
}
.placeholder {
  color: var(--muted);
}
</style>
