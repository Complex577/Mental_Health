<template>
  <div class="chart-container">
    <h3 class="title">{{ title }}</h3>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

defineProps({
  chartData: Object,
  title: String
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, // still needed
  plugins: {
    legend: { display: false },
    tooltip: { mode: 'index', intersect: false },
    title: { display: false }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { color: '#333' },
      grid: { color: '#eee' }
    },
    x: {
      ticks: { color: '#333' },
      grid: { display: false }
    }
  }
}
</script>

<style scoped>
.chart-container {
  height: 300px; /* ✅ ADD THIS */
  padding: 1rem;
}
</style>
