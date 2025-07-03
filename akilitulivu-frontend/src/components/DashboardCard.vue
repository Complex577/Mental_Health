<template>
  <div class="card" @click="$emit('click')">
    <div class="icon"><img :src="icon" alt="icon"></div>
    <div class="label">{{ title }}</div>
    <p>{{ description }}</p>
  </div>
</template>

<script>
export default {
  props: ["icon", "title", "description"]
}
</script>

<style scoped>
.card {
  background: var(--light-pink);
  border-left: 6px solid var(--primary-red);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.1);
}
.icon {
  font-size: 2rem;
  margin-bottom: 10px;
}
.label {
  font-weight: 600;
  font-size: 1.1rem;
}
img {
  width: 70px;
  height: 70px;
}
</style>
