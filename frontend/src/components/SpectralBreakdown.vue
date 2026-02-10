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

  // Generate varied blue shades
  const colors = labels.map((_, i) => {
    const hue = 220 + (i % 5) * 8
    const saturation = 70 + (i % 3) * 10
    const lightness = 50 + (i % 4) * 8
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`
  })

  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor: colors,
        borderColor: '#2d3548',
        borderWidth: 2
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
        color: '#a3a3a3',
        font: {
          family: "system-ui, sans-serif",
          size: 12,
          weight: '500'
        },
        padding: 12,
        boxWidth: 12,
        boxHeight: 12
      }
    },
    tooltip: {
      backgroundColor: 'rgba(26, 26, 26, 0.95)',
      titleColor: '#f5f5f5',
      bodyColor: '#d4d4d4',
      borderColor: '#888888',
      borderWidth: 1,
      padding: 12,
      titleFont: {
        size: 13,
        weight: '600'
      },
      bodyFont: {
        size: 13
      },
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
  height: 320px;
  position: relative;
  padding: 0.5rem;
}

.no-data {
  color: var(--text-tertiary);
  text-align: center;
  padding: 4rem 2rem;
  opacity: 0.6;
  font-size: 0.9375rem;
}
</style>
