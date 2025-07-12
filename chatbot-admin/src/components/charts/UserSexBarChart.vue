<template>
  <Bar :data="chartData" :options="options" />
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps(['data'])

const chartData = {
  labels: props.data.map(item => `${item.user_type} (${item.sex})`),
  datasets: [{
    label: 'Count',
    backgroundColor: '#f87070',
    data: props.data.map(item => item.count)
  }]
}

const options = {
  responsive: true,
  plugins: { legend: { display: false } },
  animation: { duration: 1000 }
}
</script>
