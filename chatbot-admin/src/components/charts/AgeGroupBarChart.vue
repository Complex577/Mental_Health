<template>
  <Bar :data="chartData" :options="options" />
</template>

<script setup>
import { Bar } from 'vue-chartjs'

const props = defineProps(['data'])

const chartData = {
  labels: props.data.map(g => g.age_group),
  datasets: [{
    label: 'Assessments',
    backgroundColor: '#FFB6C1',
    data: props.data.map(g => g.count)
  }]
}

const options = {
  responsive: true,
  plugins: { legend: { display: false } },
  animation: { duration: 800 }
}
</script>
