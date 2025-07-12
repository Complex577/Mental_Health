<template>
  <div class="stat-card">
    <i :class="['icon', `fas fa-${icon}`]"></i>
    <div class="content">
      <p class="value">{{ value }}</p>
      <p class="title">{{ title }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps(['title', 'value', 'icon'])
</script>

<style scoped>
.stat-card {
  background: var(--light-pink);
  border-left: 5px solid var(--primary-red);
  padding: 1rem;
  border-radius: 10px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}
.stat-card:hover {
  transform: translateY(-2px);
}
.icon {
  font-size: 2rem;
  margin-right: 1rem;
  color: var(--primary-red);
}
.value {
  font-size: 1.5rem;
  font-weight: bold;
}
.title {
  color: #666;
}
</style>
