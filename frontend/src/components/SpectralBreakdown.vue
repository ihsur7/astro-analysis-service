<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { useCatalogStore } from '../stores/catalog'

ChartJS.register(ArcElement, Tooltip, Legend)

const store = useCatalogStore()

const chartData = computed(() => {
  const breakdown = store.spectralBreakdown
  if (!breakdown || Object.keys(breakdown).length === 0) {
    return { labels: [], datasets: [] }
  }

  const labels = Object.keys(breakdown)
  const data = Object.values(breakdown)

  // Generate varied green shades
  const colors = labels.map((_, i) => {
    const hue = 120 // Green
    const saturation = 70 + (i % 3) * 10
    const lightness = 40 + (i % 5) * 8
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`
  })

  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor: colors,
        borderColor: '#00ff41',
        borderWidth: 1
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right' as const,
      labels: {
        color: '#00cc33',
        font: {
          family: "'Courier New', monospace"
        },
        padding: 10
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 26, 13, 0.95)',
      titleColor: '#00ff41',
      bodyColor: '#00ff41',
      borderColor: '#00ff41',
      borderWidth: 1,
      callbacks: {
        label: function(context: any) {
          const label = context.label || ''
          const value = context.parsed || 0
          const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0)
          const percentage = ((value / total) * 100).toFixed(1)
          return `${label}: ${value} (${percentage}%)`
        }
      }
    }
  }
}
</script>

<template>
  <div class="chart-container">
    <Doughnut v-if="chartData.labels.length > 0" :data="chartData" :options="chartOptions" />
    <div v-else class="no-data">Loading...</div>
  </div>
</template>

<style scoped>
.chart-container {
  height: 300px;
  position: relative;
}

.no-data {
  color: #00cc33;
  text-align: center;
  padding: 2rem;
  opacity: 0.6;
}
</style>
