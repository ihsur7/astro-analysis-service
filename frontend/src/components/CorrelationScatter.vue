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
        backgroundColor: 'rgba(0, 255, 65, 0.5)',
        borderColor: 'rgba(0, 255, 65, 0.8)',
        borderWidth: 1,
        pointRadius: 3,
        pointHoverRadius: 5
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
      borderWidth: 1,
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
        text: 'Apparent Magnitude (lower = brighter)',
        color: '#00ff41'
      },
      ticks: {
        color: '#00cc33'
      },
      grid: {
        color: 'rgba(0, 255, 65, 0.1)'
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
}

.no-data {
  color: #00cc33;
  text-align: center;
  padding: 2rem;
  opacity: 0.6;
}
</style>
