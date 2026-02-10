<script setup lang="ts">
import { computed } from 'vue'
import { Scatter } from 'vue-chartjs'
import { Chart as ChartJS, LinearScale, PointElement, Tooltip, Legend } from 'chart.js'
import { useCatalogStore } from '../stores/catalog'

ChartJS.register(LinearScale, PointElement, Tooltip, Legend)

const store = useCatalogStore()

const chartData = computed(() => {
  const corr = store.correlation
  if (!corr || !corr.magnitudes || corr.magnitudes.length === 0) {
    return { datasets: [] }
  }

  const data = corr.magnitudes.map((mag: number, i: number) => ({
    x: corr.distances[i],
    y: mag
  }))

  return {
    datasets: [
      {
        label: 'Exoplanet Hosts',
        data,
        backgroundColor: 'rgba(245, 158, 11, 0.5)',
        borderColor: 'rgba(245, 158, 11, 0.8)',
        borderWidth: 1,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: 'rgba(245, 158, 11, 1)',
        pointHoverBorderColor: '#fff',
        pointHoverBorderWidth: 2
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
      borderColor: '#f59e0b',
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
          return `Magnitude: ${context.parsed.y.toFixed(2)}, Distance: ${context.parsed.x.toFixed(1)} ly`
        }
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
        text: 'Apparent Magnitude (lower = brighter)',
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
      },
      reverse: false
    }
  }
}
</script>

<template>
  <div class="chart-container">
    <Scatter v-if="chartData.datasets.length > 0" :data="chartData" :options="chartOptions" />
    <div v-else class="no-data">Loading...</div>
  </div>
</template>

<style scoped>
.chart-container {
  height: 400px;
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
