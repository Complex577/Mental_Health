<template>
  <div class="education-manager">
    <h2 class="title">Education Content Management</h2>

    <div class="toolbar">
      <select v-model="selectedType" @change="fetchNodes">
        <option value="user">User Education</option>
        <option value="teacher">Teacher Training</option>
        <option value="parent">Parent Training</option>
      </select>
      <button @click="showModal = true"><i class="fas fa-plus"></i> New Root Topic</button>
    </div>

    <div v-if="loading" class="loader">Loading...</div>

    <div v-else class="node-list">
      <NodeItem
        v-for="node in nodes"
        :key="node.id"
        :node="node"
        @refresh="fetchNodes"
      />
    </div>

    <!-- Modal for Adding Root Topic -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h3>Add Root Topic</h3>
        <label>Title (EN):</label>
        <input v-model="newNode.title_en" type="text" />
        <label>Title (SW):</label>
        <input v-model="newNode.title_sw" type="text" />
        <label>Content (EN):</label>
        <textarea v-model="newNode.content_en" rows="3"></textarea>
        <label>Content (SW):</label>
        <textarea v-model="newNode.content_sw" rows="3"></textarea>

        <div class="modal-actions">
          <button @click="submitRootNode">Submit</button>
          <button class="cancel" @click="showModal = false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../services/api'
import NodeItem from './NodeItem.vue'

const selectedType = ref('user')
const nodes = ref([])
const loading = ref(false)
const showModal = ref(false)

const newNode = ref({
  title_en: '',
  title_sw: '',
  content_en: '',
  content_sw: ''
})

const fetchNodes = async () => {
  loading.value = true
  const res = await axios.get(`/api/admin/content-nodes/?type=${selectedType.value}`)
  nodes.value = res.data
  loading.value = false
}

const submitRootNode = async () => {
  if (!newNode.value.title_en.trim()) return alert('English title is required.')

  await axios.post('/api/admin/create/content-nodes/', {
    ...newNode.value,
    node_type: selectedType.value
  })

  showModal.value = false
  newNode.value = { title_en: '', title_sw: '', content_en: '', content_sw: '' }
  fetchNodes()
}

onMounted(fetchNodes)
</script>

<style scoped>
.education-manager {
  padding: 1rem;
}
.title {
  color: var(--primary-red);
  margin-bottom: 1rem;
}
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
select {
  padding: 0.5rem;
  border-radius: 5px;
}
button {
  background: var(--primary-red);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
}
button.cancel {
  background: #999;
}
.node-list {
  padding-left: 0.5rem;
}
.loader {
  text-align: center;
  color: #999;
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal {
  background: white;
  padding: 2rem;
  width: 400px;
  max-width: 90%;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0,0,0,0.2);
}
.modal h3 {
  margin-bottom: 1rem;
  color: var(--primary-red);
}
.modal label {
  display: block;
  margin-top: 1rem;
  font-weight: bold;
}
.modal input,
.modal textarea {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.25rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}
.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}
</style>
