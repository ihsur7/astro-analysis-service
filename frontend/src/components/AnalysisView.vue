<script setup lang="ts">
import { onMounted, ref } from 'vue'
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
      <h2>Dataset Analysis</h2>
      <button @click="loadAnalysis" :disabled="loading" class="refresh-btn">
        {{ loading ? 'Loading...' : 'Refresh' }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else class="charts-grid">
      <div class="chart-card">
        <h3>Magnitude Distribution</h3>
        <p class="chart-description">Brightness distribution of exoplanet host stars (lower = brighter)</p>
        <MagnitudeDistribution />
      </div>

      <div class="chart-card">
        <h3>Spectral Type Breakdown</h3>
        <p class="chart-description">Classification of stars by spectral type</p>
        <SpectralBreakdown />
      </div>

      <div class="chart-card">
        <h3>Distance Distribution</h3>
        <p class="chart-description">Distribution of exoplanet hosts by distance (light years)</p>
        <DistanceDistribution />
      </div>

      <div class="chart-card full-width">
        <h3>Magnitude vs Distance Correlation</h3>
        <p class="chart-description">Observational bias: brighter stars surveyed at greater distances</p>
        <CorrelationScatter />
      </div>
    </div>
  </div>
</template>

<style scoped>
.analysis-view {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.analysis-header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #00ff41;
}

.refresh-btn {
  background: #003311;
  color: #00ff41;
  border: 1px solid #00ff41;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-family: 'Courier New', monospace;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #00ff41;
  color: #000;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  background: #330000;
  border: 1px solid #ff0000;
  color: #ff4444;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
}

.chart-card {
  background: #001a0d;
  border: 1px solid #00ff41;
  padding: 1.5rem;
  border-radius: 4px;
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-card h3 {
  margin: 0 0 0.5rem 0;
  color: #00ff41;
  font-size: 1.2rem;
}

.chart-description {
  margin: 0 0 1rem 0;
  color: #00cc33;
  font-size: 0.9rem;
  opacity: 0.8;
}

@media (max-width: 1100px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
