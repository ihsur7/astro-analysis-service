<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { useCatalogStore } from '../stores/catalog'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const store = useCatalogStore()

const chartData = computed(() => {
  const dist = store.distanceDistribution
  if (!dist || !dist.bins || dist.bins.length === 0) {
    return { labels: [], datasets: [] }
  }

  return {
    labels: dist.bins.map((b: number) => b.toFixed(0)),
    datasets: [
      {
        label: 'Number of Objects',
        data: dist.counts,
        backgroundColor: 'rgba(16, 185, 129, 0.6)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 1,
        borderRadius: 4
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(26, 26, 26, 0.95)',
      titleColor: '#f5f5f5',
      bodyColor: '#d4d4d4',
      borderColor: '#10b981',
      borderWidth: 1,
      padding: 12,
      titleFont: {
        size: 13,
        weight: '600'
      },
      bodyFont: {
        size: 13
      }
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Distance (light years)',
        color: '#a3a3a3',
        font: {
          size: 12,
          weight: '600'
        }
      },
      ticks: {
        color: '#64748b'
      },
      grid: {
        color: 'rgba(45, 53, 72, 0.5)',
        drawBorder: false
      }
    },
    y: {
      title: {
        display: true,
        text: 'Count',
        color: '#94a3b8',
        font: {
          size: 12,
          weight: '600'
        }
      },
      ticks: {
        color: '#64748b'
      },
      grid: {
        color: 'rgba(45, 53, 72, 0.5)',
        drawBorder: false
      }
    }
  }
}
</script>

<template>
  <div class="chart-container">
    <Bar v-if="chartData.labels.length > 0" :data="chartData" :options="chartOptions" />
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
