<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { useCatalogStore } from '../stores/catalog'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const store = useCatalogStore()

const chartData = computed(() => {
  const dist = store.magnitudeDistribution
  if (!dist || !dist.bins || dist.bins.length === 0) {
    return { labels: [], datasets: [] }
  }

  return {
    labels: dist.bins.map((b: number) => b.toFixed(1)),
    datasets: [
      {
        label: 'Number of Objects',
        data: dist.counts,
        backgroundColor: 'rgba(0, 255, 65, 0.6)',
        borderColor: 'rgba(0, 255, 65, 1)',
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
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(0, 26, 13, 0.95)',
      titleColor: '#00ff41',
      bodyColor: '#00ff41',
      borderColor: '#00ff41',
      borderWidth: 1
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Apparent Magnitude',
        color: '#00ff41'
      },
      ticks: {
        color: '#00cc33'
      },
      grid: {
        color: 'rgba(0, 255, 65, 0.1)'
      }
    },
    y: {
      title: {
        display: true,
        text: 'Count',
        color: '#00ff41'
      },
      ticks: {
        color: '#00cc33'
      },
      grid: {
        color: 'rgba(0, 255, 65, 0.1)'
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
