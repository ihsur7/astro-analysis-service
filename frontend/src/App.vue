<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="header-content">
        <div class="logo-section">
          <Telescope class="logo-icon" :size="32" :stroke-width="2" />
          <div>
            <h1 class="app-title">Astro Analysis</h1>
            <p class="app-subtitle">NASA Exoplanet Archive Explorer</p>
          </div>
        </div>
        <div class="header-actions">
          <button @click="showSettings = true" class="header-button settings-btn" title="Settings">
            <Settings :size="18" />
          </button>
          <a href="/docs" target="_blank" rel="noreferrer" class="header-link">
            <BookOpen :size="16" />
            <span>API Docs</span>
          </a>
          <a href="https://exoplanetarchive.ipac.caltech.edu/" target="_blank" rel="noreferrer" class="header-link">
            <Database :size="16" />
            <span>Data Source</span>
            <ExternalLink :size="14" />
          </a>
        </div>
      </div>
    </header>

    <nav class="tabs-nav">
      <button 
        :class="{ active: activeTab === 'catalog' }" 
        @click="activeTab = 'catalog'"
        class="tab-button"
      >
        <Table2 :size="18" />
        <span>Catalog</span>
      </button>
      <button 
        :class="{ active: activeTab === 'analysis' }" 
        @click="activeTab = 'analysis'"
        class="tab-button"
      >
        <BarChart3 :size="18" />
        <span>Analysis</span>
      </button>
    </nav>

    <main class="main-content">
      <div v-show="activeTab === 'catalog'" class="catalog-view">
        <StatusBar />
        <section class="content-grid">
          <FiltersPanel />
          <StatsPanel />
        </section>
        <ObjectsTable />
        <PaginationControls />
      </div>

      <div v-show="activeTab === 'analysis'" class="analysis-view">
        <AnalysisView />
      </div>
    </main>

    <SettingsModal :show="showSettings" @close="showSettings = false" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from "vue";
import { Telescope, BookOpen, Database, ExternalLink, Table2, BarChart3, Settings } from 'lucide-vue-next';
import FiltersPanel from "./components/FiltersPanel.vue";
import StatsPanel from "./components/StatsPanel.vue";
import ObjectsTable from "./components/ObjectsTable.vue";
import PaginationControls from "./components/PaginationControls.vue";
import StatusBar from "./components/StatusBar.vue";
import AnalysisView from "./components/AnalysisView.vue";
import SettingsModal from "./components/SettingsModal.vue";
import { useCatalogStore } from "./stores/catalog";

const catalog = useCatalogStore();
const activeTab = ref<'catalog' | 'analysis'>('catalog');
const showSettings = ref(false);

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
  min-height: 100vh;
}

.app-header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 1.5rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  background: rgba(26, 26, 26, 0.95);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  color: var(--primary);
  flex-shrink: 0;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.app-subtitle {
  font-size: 0.875rem;
  color: var(--text-tertiary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.header-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.625rem;
  border-radius: 0.5rem;
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.header-button:hover {
  background: var(--surface-hover);
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
}

.header-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
}

.header-link:hover {
  background: var(--surface-hover);
  border-color: var(--primary);
  color: var(--primary);
}

.tabs-nav {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem 0;
  display: flex;
  gap: 0.5rem;
  border-bottom: 1px solid var(--border);
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-tertiary);
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  top: 1px;
}

.tab-button:hover {
  color: var(--text-secondary);
  background: var(--primary-light);
}

.tab-button.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }

  .header-link {
    justify-content: center;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
