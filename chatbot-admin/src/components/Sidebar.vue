<template>
  <div :class="['sidebar', { collapsed }]">
    <div class="toggle-button" @click="$emit('toggle')">
      <i :class="collapsed ? 'fas fa-bars' : 'fas fa-arrow-left'"></i>
    </div>
    <div class="logo" v-if="!collapsed">
        <!--<img :src="logo" alt="logo">-->
        FlickFlier
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
        { name: 'Visits Rate', path: '/admin/visits' },
        { name: 'Predictions', path: '/admin/predictions' },
        { name: 'Compose Email', path: '/admin/compose' },
        { name: 'Send Email', path: '/admin/send' },
        { name: 'Logout', path: '/admin/logout' }
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
  background: linear-gradient(to bottom, #203a43, #2c5364);
  color: white;
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
  right: -45px;
  background: var(--secondary-color);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
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
  border-radius: 50%;
  object-fit: cover;
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
  color: var(--text-color);
  font-size: 14px;
  text-decoration: none;
  transition: 0.2s ease;
}
a:hover {
  color: #00c6ff;
}
.router-link-active {
  color: #00c6ff;
}
</style>
