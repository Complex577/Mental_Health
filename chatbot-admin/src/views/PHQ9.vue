<template>
  <div class="phq9-dashboard">
    <Loader v-if="loading" />

    <div v-else>
      <h2 class="title">PHQ-9 Assessment Analytics</h2>

      <div class="stats-grid">
        <StatCard title="Total Assessments" :value="totalAssessments" icon="fas fa-list" />
        <StatCard title="Average Score" :value="averageScore" icon="bar-chart" />
        <StatCard title="High Risk Cases" :value="highRiskCount" icon="fas fa-exclamation-triangle" class="high-risk" />
        <StatCard title="Last Submission" :value="formatDate(lastUpdated)" icon="clock" />
      </div>

      <div class="bars">
        <div class="chart-section">
          <h3>User Type & Sex Distribution</h3>
          <BarChart :data="userSexChartData" />
        </div>

        <div class="chart-section">
          <h3>Age Group Distribution</h3>
          <AgeGroupChart :data="ageGroupChartData" />
        </div>
      </div>

      <div class="chart-section pie">
        <h3>Score Range Breakdown</h3>
        <ScoreRangeChart :data="scoreRangeData" />
      </div>

      <div class="raw-table">
        <h3>Recent Submissions</h3>
        <DataTable :rows="recentAssessments" />
      </div>
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
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  color: var(--primary-red);
  margin-bottom: 1rem;
  font-size: 1.5rem;
  text-align: left;
}

.stats-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  gap: 16px;
  margin-bottom: 1.5rem;
}

.stats-grid > * {
  flex: 1 1 180px;
  max-width: 220px;
}

.bars {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  gap: 16px;
  margin-bottom: 2rem;
}

.chart-section {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
  padding: 1rem;
  flex: 1 1 300px;
  max-width: 500px;
  width: 100%;
}

.pie {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
  text-align: center;
}

.raw-table {
  background: #fff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.07);
  margin-top: 2rem;
  overflow-x: auto;
}

/* Responsive Enhancements */
@media (max-width: 768px) {
  .stats-grid, .bars {
    flex-direction: column;
    align-items: center;
  }

  .chart-section, .pie {
    width: 100%;
    max-width: 100%;
  }

  .stats-grid > * {
    width: 100%;
    max-width: 100%;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
