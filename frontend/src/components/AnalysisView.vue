<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { BarChart3, RefreshCw, AlertCircle } from 'lucide-vue-next'
import { useCatalogStore } from '../stores/catalog'
import MagnitudeDistribution from './MagnitudeDistribution.vue'
import SpectralBreakdown from './SpectralBreakdown.vue'
import DistanceDistribution from './DistanceDistribution.vue'
import CorrelationScatter from './CorrelationScatter.vue'

const store = useCatalogStore()
const loading = ref(false)
const error = ref<string | null>(null)

async function loadAnalysis() {
  loading.value = true
  error.value = null
  try {
    await Promise.all([
      store.fetchMagnitudeDistribution(),
      store.fetchSpectralBreakdown(),
      store.fetchDistanceDistribution(),
      store.fetchCorrelation()
    ])
  } catch (e: any) {
    error.value = e.message || 'Failed to load analysis data'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAnalysis()
})
</script>

<template>
  <div class="analysis-view">
    <div class="analysis-header">
      <div class="header-title">
        <BarChart3 :size="24" />
        <div>
          <h2>Dataset Analysis</h2>
          <p class="header-subtitle">Statistical insights and visualizations</p>
        </div>
      </div>
      <button @click="loadAnalysis" :disabled="loading" class="refresh-btn">
        <RefreshCw :size="16" :class="{ spin: loading }" />
        <span>{{ loading ? 'Loading...' : 'Refresh' }}</span>
      </button>
    </div>

    <div v-if="error" class="error-banner">
      <AlertCircle :size="20" />
      <span>{{ error }}</span>
    </div>

    <div v-else class="charts-grid">
      <div class="chart-card">
        <div class="chart-header">
          <h3>Magnitude Distribution</h3>
          <p class="chart-description">Brightness distribution of exoplanet host stars (lower = brighter)</p>
        </div>
        <MagnitudeDistribution />
      </div>

      <div class="chart-card">
        <div class="chart-header">
          <h3>Spectral Type Breakdown</h3>
          <p class="chart-description">Classification of stars by spectral type</p>
        </div>
        <SpectralBreakdown />
      </div>

      <div class="chart-card">
        <div class="chart-header">
          <h3>Distance Distribution</h3>
          <p class="chart-description">Distribution of exoplanet hosts by distance (light years)</p>
        </div>
        <DistanceDistribution />
      </div>

      <div class="chart-card full-width">
        <div class="chart-header">
          <h3>Magnitude vs Distance Correlation</h3>
          <p class="chart-description">Observational bias: brighter stars surveyed at greater distances</p>
        </div>
        <CorrelationScatter />
      </div>
    </div>
  </div>
</template>

<style scoped>
.analysis-view {
  padding: 0;
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: var(--primary);
}

.header-title h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.header-subtitle {
  margin: 0.25rem 0 0 0;
  font-size: 0.875rem;
  color: var(--text-tertiary);
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(136, 136, 136, 0.3);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.error-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 0.75rem;
  color: var(--error);
  margin-bottom: 2rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 1.5rem;
}

.chart-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: border-color 0.2s;
}

.chart-card:hover {
  border-color: var(--primary-border);
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-header {
  margin-bottom: 1.5rem;
}

.chart-card h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
  font-size: 1.125rem;
  font-weight: 600;
}

.chart-description {
  margin: 0;
  color: var(--text-tertiary);
  font-size: 0.875rem;
  line-height: 1.5;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 1100px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .analysis-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .refresh-btn {
    justify-content: center;
  }
}
</style>
