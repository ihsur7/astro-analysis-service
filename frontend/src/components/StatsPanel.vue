<template>
  <section class="stats-panel">
    <header class="panel-header">
      <div class="header-title">
        <TrendingUp :size="20" />
        <h2>Statistics</h2>
      </div>
      <div v-if="stats" class="total-badge">
        <span class="total-count">{{ stats.count.toLocaleString() }}</span>
        <span class="total-label">objects</span>
      </div>
    </header>
    
    <div v-if="stats" class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <Minimize2 :size="16" />
        </div>
        <div class="stat-content">
          <span class="stat-label">Magnitude Range</span>
          <strong class="stat-value">{{ format(stats.magnitude_min) }} - {{ format(stats.magnitude_max) }}</strong>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <BarChart2 :size="16" />
        </div>
        <div class="stat-content">
          <span class="stat-label">Average Magnitude</span>
          <strong class="stat-value">{{ format(stats.magnitude_avg) }}</strong>
        </div>
      </div>
      
      <div class="stat-card highlight">
        <div class="stat-icon">
          <Sun :size="16" />
        </div>
        <div class="stat-content">
          <span class="stat-label">Brightest Object</span>
          <strong class="stat-value">{{ stats.brightest_object?.name ?? "N/A" }}</strong>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <Moon :size="16" />
        </div>
        <div class="stat-content">
          <span class="stat-label">Dimmest Object</span>
          <strong class="stat-value">{{ stats.dimmest_object?.name ?? "N/A" }}</strong>
        </div>
      </div>
    </div>
    
    <div v-else class="no-data">
      <AlertCircle :size="20" />
      <p>No statistics available. Refresh to load data.</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { TrendingUp, Minimize2, BarChart2, Sun, Moon, AlertCircle } from 'lucide-vue-next';
import { useCatalogStore } from "../stores/catalog";

const catalog = useCatalogStore();
const { stats } = storeToRefs(catalog);

const format = (value: number | null) => {
  if (value === null || value === undefined) return "—";
  return typeof value === 'number' ? value.toFixed(2) : "—";
};
</script>

<style scoped>
.stats-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
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

.total-badge {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  border-radius: 0.5rem;
}

.total-count {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
}

.total-label {
  font-size: 0.875rem;
  color: var(--text-tertiary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.stat-card:hover {
  background: var(--surface-hover);
  border-color: var(--primary-border);
}

.stat-card.highlight {
  background: var(--primary-light);
  border-color: var(--primary-border);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background: var(--surface);
  border-radius: 0.5rem;
  color: var(--primary);
  flex-shrink: 0;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 2rem;
  color: var(--text-tertiary);
  text-align: center;
}

.no-data p {
  margin: 0;
  font-size: 0.9375rem;
}
</style>
