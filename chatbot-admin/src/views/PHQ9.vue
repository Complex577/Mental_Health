<template>
  <div class="phq9-dashboard">
    <Loader v-if="loading" />

    <div v-else>
      <h2 class="title">PHQ-9 Assessment Analytics</h2>

      
      <section class="stats-grid">
        <StatCard title="Total Assessments" :value="totalAssessments" icon="fas fa-list" />
        <StatCard title="Average Score" :value="averageScore" icon="bar-chart" />
        <StatCard title="High Risk Cases" :value="highRiskCount" icon="fas fa-exclamation-triangle" class="high-risk" />
        <StatCard title="Last Submission" :value="formatDate(lastUpdated)" icon="clock" />
      </section>

      <div class="bars">
      <section class="chart-section">
        <h3>User Type & Sex Distribution</h3>
        <BarChart :data="userSexChartData" />
      </section>

      <section class="chart-section">
        <h3>Age Group Distribution</h3>
        <AgeGroupChart :data="ageGroupChartData" />
      </section>
      </div>

      <section class="chart-section pie">
        <h3>Score Range Breakdown</h3>
        <ScoreRangeChart :data="scoreRangeData" />
      </section>

      <section class="raw-table">
        <h3>Recent Submissions</h3>
        <DataTable :rows="recentAssessments" />
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Loader from '../components/ui/Loader.vue'
import StatCard from '../components/ui/StatCard.vue'
import BarChart from '../components/charts/UserSexBarChart.vue'
import AgeGroupChart from '../components/charts/AgeGroupBarChart.vue'
import ScoreRangeChart from '../components/charts/ScorePieChart.vue'
import DataTable from '../components/ui/RecentAssessmentTable.vue'
import axios from '../services/api'

const loading = ref(true)
const totalAssessments = ref(0)
const averageScore = ref(0)
const highRiskCount = ref(0)
const lastUpdated = ref('')
const userSexChartData = ref([])
const ageGroupChartData = ref([])
const scoreRangeData = ref([])
const recentAssessments = ref([])

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/admin/phq9-stats')
    totalAssessments.value = data.total
    averageScore.value = data.average_score
    highRiskCount.value = data.high_risk
    lastUpdated.value = data.last_updated
    userSexChartData.value = data.user_sex_chart
    ageGroupChartData.value = data.age_group_chart
    scoreRangeData.value = data.score_ranges
    recentAssessments.value = data.recent
  } catch (err) {
    console.error('Error fetching PHQ-9 data:', err)
  } finally {
    loading.value = false
  }
})
const formatDate = (datetime) => {
  if (!datetime) return 'N/A'
  return new Date(datetime).toLocaleString()
}

</script>

<style scoped>
.phq9-dashboard {
  padding: 1rem;
  animation: fadeIn 0.6s ease-in;
}
.title {
  color: var(--primary-red);
  margin-bottom: 1rem;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.bars {
    display: flex;
    justify-content:center;
    gap: 3px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.chart-section {
  margin-bottom: 2rem;
  background-color: white;
  width: 95%;
  max-width: 500px;
  margin: 0 auto;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0,0,0,0.05);
  padding: 1rem;
}
.pie {
    width: 100%;
    height: 600px;
    max-width: 900px;
}
.raw-table {
  background: #fff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.07);
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
