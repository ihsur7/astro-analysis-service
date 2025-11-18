<template>
  <section class="panel stats">
    <header>
      <h2>Dataset Stats</h2>
      <small v-if="stats">{{ stats.count }} objects</small>
    </header>
    <div v-if="stats" class="grid">
      <article>
        <span>Magnitude range</span>
        <strong>{{ format(stats.magnitude_min) }} – {{ format(stats.magnitude_max) }}</strong>
      </article>
      <article>
        <span>Average magnitude</span>
        <strong>{{ format(stats.magnitude_avg) }}</strong>
      </article>
      <article>
        <span>Brightest</span>
        <strong>{{ stats.brightest_object?.name ?? "n/a" }}</strong>
      </article>
      <article>
        <span>Dimmest</span>
        <strong>{{ stats.dimmest_object?.name ?? "n/a" }}</strong>
      </article>
    </div>
    <p v-else class="placeholder">No stats yet. Trigger a refresh.</p>
  </section>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useCatalogStore } from "../stores/catalog";

const catalog = useCatalogStore();
const { stats } = storeToRefs(catalog);

const format = (value: number | null) => (value ?? "—");
</script>

<style scoped>
.panel {
  background: var(--panel);
  border: 1px solid var(--accent-muted);
  border-radius: 16px;
  padding: 1.5rem;
}
header {
  display: flex;
  justify-content: space-between;
  color: var(--muted);
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
article {
  padding: 0.75rem;
  border-radius: 12px;
  background: rgba(148, 163, 184, 0.08);
}
span {
  font-size: 0.75rem;
  color: var(--muted);
}
strong {
  display: block;
  margin-top: 0.35rem;
  font-size: 1.1rem;
}
.placeholder {
  color: var(--muted);
}
</style>
