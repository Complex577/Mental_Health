<template>
  <div class="admin-layout">
    <Sidebar :collapsed="sidebarCollapsed" @toggle="toggleSidebar" />

    <div :class="['main-content', { collapsed: sidebarCollapsed }]">
      <header class="top-bar">
        <h3>Mental Health</h3>
        <button class="compose-btn"><i class="fas fa-user"></i> Complex</button>
      </header>

      <section class="router-view-wrapper">
        <router-view />
      </section>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'

export default {
  name: 'AdminLayout',
  components: { Sidebar },
  data() {
    return {
      sidebarCollapsed: false
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    }
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.main-content {
  flex: 1;
  transition: margin-left 0.3s ease;
  margin-left: 250px;
  display: flex;
  flex-direction: column;
}
.main-content.collapsed {
  margin-left: 70px;
}

.top-bar {
  height: 60px;
  border-bottom:  3px double var(--primary-red);
  display: flex;
  align-items: center;
  background-color: var(--light-pink);
  justify-content: space-between;
  padding: 0 1rem;
  color: var(--primary-red);
}
.top-bar h3 {
    color: var(--primary-red);
}

.compose-btn {
  background: var(--primary-red);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.router-view-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #f5f7fa;
}
@media(max-width: 600px) {
.main-content {
  margin-left: 0px;
  
}
.main-content.collapsed {
  margin-left: 0px;
}
.top-bar h3 {
    margin-left: 38px;
}
}
</style>
