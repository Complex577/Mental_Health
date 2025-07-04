<template>
  <div class="visits-rate-view">
    <div class="table-section">
      <h3>Most IPs Today</h3>
      <table>
        <thead>
          <tr>
            <th>IP Address</th>
            <th>Location</th>
            <th>Visits</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!loading && todayVisits.length === 0">
            <td colspan="3">No data found for today.</td>
          </tr>
          <tr v-for="entry in todayVisits" :key="entry.ip">
            <td>{{ entry.ip }}</td>
            <td>{{ entry.location }}</td>
            <td>{{ entry.visits }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="table-section">
      <h3>Top IPs This Week</h3>
      <table>
        <thead>
          <tr>
            <th>IP Address</th>
            <th>Location</th>
            <th>Visits</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!loading && weeklyVisits.length === 0">
            <td colspan="3">No data found for this week.</td>
          </tr>
          <tr v-for="entry in weeklyVisits" :key="entry.ip">
            <td>{{ entry.ip }}</td>
            <td>{{ entry.location }}</td>
            <td>{{ entry.visits }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="table-section">
      <h3>All Visitors (Paginated)</h3>
      <table>
        <thead>
          <tr>
            <th>IP Address</th>
            <th>Location</th>
            <th>Visits</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!loading && allVisitors.length === 0">
            <td colspan="3">No visitor data available.</td>
          </tr>
          <tr v-for="entry in allVisitors" :key="entry.ip">
            <td>{{ entry.ip }}</td>
            <td>{{ entry.location }}</td>
            <td>{{ entry.visits }}</td>
          </tr>
        </tbody>
      </table>

      <div class="pagination" v-if="totalPages > 1">
        <button :disabled="currentPage === 1" @click="currentPage-- && fetchPaginated()">
          Previous
        </button>
        <span>Page {{ currentPage }} <b>of</b> {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="currentPage++ && fetchPaginated()">
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VisitsRate',
  data() {
    return {
      todayVisits: [],
      weeklyVisits: [],
      allVisitors: [],
      currentPage: 1,
      totalPages: 1,
      loading: false
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const [todayRes, weekRes] = await Promise.all([
          axios.get('/api/visits/today/'),
          axios.get('/api/visits/week/')
        ])
        this.todayVisits = todayRes.data
        this.weeklyVisits = weekRes.data
        this.fetchPaginated()
      } catch (err) {
        console.error('Error fetching visits data:', err)
      } finally {
        this.loading = false
      }
    },
    async fetchPaginated() {
      this.loading = true
      try {
        const response = await axios.get(`/api/visits/all/?page=${this.currentPage}`)
        this.allVisitors = response.data.results
        this.totalPages = response.data.total_pages
      } catch (err) {
        console.error('Error fetching paginated data:', err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.visits-rate-view {
  padding: 1rem;
  color: white;
}

.table-section {
  margin-bottom: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

h2, h3 {
  margin-bottom: 1rem;
  color: #00c6ff;
}

table {
  width: 100%;
  border-collapse: collapse;
  color: #203a43;
  font-size: 11px;
}

th, td {
  text-align: left;
  padding: 0.75rem;
  border-bottom: 1px solid rgba(36, 157, 190, 0.2);
}

th {
  background-color: #2c5364;
  color: rgb(143, 118, 118);
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}
span {
  color: #2c5364;
  font-size: 11px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #00c6ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}
button:disabled {
  background-color: grey;
  cursor: not-allowed;
}
</style>
