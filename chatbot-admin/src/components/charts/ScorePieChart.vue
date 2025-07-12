<template>
  <Pie :data="chartData" :options="options" />
</template>

<script setup>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps(['data'])

const chartData = {
  labels: props.data.map(s => s.label),
  datasets: [{
    data: props.data.map(s => s.count),
    backgroundColor: ['#e57373', '#f06292', '#ba68c8', '#7986cb', '#4db6ac']
  }]
}

const options = {
  responsive: true,
  plugins: { legend: { position: 'right' } },
  animation: { duration: 900 }
}
</script>
