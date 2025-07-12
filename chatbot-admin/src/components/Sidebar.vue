<template>
  <div :class="['sidebar', { collapsed }]">
    <div class="toggle-button" @click="$emit('toggle')">
      <i :class="collapsed ? 'fas fa-bars' : 'fas fa-arrow-left'"></i>
    </div>
    <div class="logo" v-if="!collapsed">
        <img src="/assets/logo_final.png" alt="logo">
        
    </div>
    <ul v-if="!collapsed">
      <li v-for="link in links" :key="link.name">
        <router-link :to="link.path">{{ link.name }}</router-link>
        <hr>
      </li>
    </ul>
  </div>
</template>

<script>
import logo from '../assets/logo.jpg'
export default {
  name: 'Sidebar',
  props: {
    collapsed: Boolean
  },
  data() {
    return {
        logo,
      links: [
        { name: 'Dashboard', path: '/admin/dashboard' },
        { name: 'PHQ-9', path: '/admin/phq9' },
        { name: 'GAD-7', path: '/admin/gad7' },
        { name: 'SDQ', path: '/admin/sdq' },
        { name: 'Referals', path: '/admin/referals' },
        { name: 'Education', path: '/admin/education' },
        { name: 'Profile', path: '/admin/profile' }
      ]
    }
  }
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 150px;
  background: var(--light-pink);
  color: var(--text-dark);
  border-top-right-radius: 20px;
  padding: 1rem;
  z-index: 1001;
  transition: transform 0.3s ease;
}

.sidebar.collapsed {
  transform: translateX(-100%);
}

.toggle-button {
  position: absolute;
  top: 10px;
  right: -50px;
  background: var(--light-pink);
  border: 1px solid var(--primary-red);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: var(--primary-red);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 1002;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #00c6ff;
  margin-bottom: 2rem;
  text-align: center;
}
.logo img {
  width: 80px;
  height: 80px;
  
  margin: 0 auto;
  display: block;
}


ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
li {
  margin-bottom: 1rem;
}
a {
  color: var(--text-dark);
  font-size: 14px;
  text-decoration: none;
  font-weight: bold;
  transition: 0.2s ease;
}
a:hover {
  color: var(--primary-red);
}
.router-link-active {
  color: var(--primary-red);
}
</style>
