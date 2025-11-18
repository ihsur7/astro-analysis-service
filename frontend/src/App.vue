<template>
  <div class="app-shell">
    <header class="hero">
      <div>
        <p class="eyebrow">astro-analysis-service</p>
        <h1>Live catalog insights</h1>
        <p class="subtitle">Filter, paginate, and benchmark stellar objects sourced from NASA.</p>
      </div>
      <div class="hero-actions">
        <a href="/docs" target="_blank" rel="noreferrer">Open API docs</a>
        <a href="https://exoplanetarchive.ipac.caltech.edu/" target="_blank" rel="noreferrer">Data source ↗</a>
      </div>
    </header>

    <nav class="tabs">
      <button 
        :class="{ active: activeTab === 'catalog' }" 
        @click="activeTab = 'catalog'"
      >
        📊 Catalog
      </button>
      <button 
        :class="{ active: activeTab === 'analysis' }" 
        @click="activeTab = 'analysis'"
      >
        📈 Analysis
      </button>
    </nav>

    <div v-show="activeTab === 'catalog'">
      <StatusBar />
      <section class="grid">
        <FiltersPanel />
        <StatsPanel />
      </section>
      <ObjectsTable />
      <PaginationControls />
    </div>

    <div v-show="activeTab === 'analysis'">
      <AnalysisView />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from "vue";
import FiltersPanel from "./components/FiltersPanel.vue";
import StatsPanel from "./components/StatsPanel.vue";
import ObjectsTable from "./components/ObjectsTable.vue";
import PaginationControls from "./components/PaginationControls.vue";
import StatusBar from "./components/StatusBar.vue";
import AnalysisView from "./components/AnalysisView.vue";
import { useCatalogStore } from "./stores/catalog";

const catalog = useCatalogStore();
const activeTab = ref<'catalog' | 'analysis'>('catalog');

const handleShortcut = (event: KeyboardEvent) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "r") {
    event.preventDefault();
    catalog.refresh();
  }
};

onMounted(() => {
  catalog.refresh();
  window.addEventListener("keydown", handleShortcut);
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleShortcut);
});
</script>

<style scoped>
.app-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}
.hero {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.25rem;
}
.eyebrow {
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.3em;
  font-size: 0.75rem;
}
h1 {
  margin: 0.35rem 0;
  font-size: 2.4rem;
}
.subtitle {
  color: var(--muted);
  max-width: 42ch;
}
.hero-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: flex-end;
}
.hero-actions a {
  color: var(--accent);
  text-decoration: none;
}
.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(0, 255, 65, 0.2);
  padding-bottom: 0.5rem;
}
.tabs button {
  background: transparent;
  border: none;
  color: var(--muted);
  font-size: 1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 2px solid transparent;
  font-family: 'Courier New', monospace;
}
.tabs button:hover {
  color: var(--accent);
}
.tabs button.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}
@media (max-width: 768px) {
  .hero {
    flex-direction: column;
  }
  .hero-actions {
    align-items: flex-start;
  }
}
</style>
