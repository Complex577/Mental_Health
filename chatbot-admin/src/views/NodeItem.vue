<template>
  <div class="node-item">
    <div class="node-header" @click="toggleExpanded">
      <span>{{ expanded ? '▼' : '▶' }}</span>
      <h3>{{ node.title_en }}</h3>
    </div>

    <div class="node-toolbar">
      <button @click.stop="showEdit = true"><i class="fas fa-pencil"></i> Edit</button>
      <button @click.stop="showAdd = true"><i class="fas fa-plus"></i> Add Subtopic</button>
      <button @click.stop="showDelete = true"><i class="fas fa-bin"></i> Delete</button>
    </div>

    <div v-if="expanded" class="node-body">
      <div class="content-block">
        <p><strong>EN:</strong> {{ node.content_en || 'No content yet.' }}</p>
        <p><strong>SW:</strong> {{ node.content_sw || 'Hakuna maudhui.' }}</p>
      </div>
      <NodeItem
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        @refresh="$emit('refresh')"
      />
    </div>

    <!-- Edit Modal -->
    <div v-if="showEdit" class="modal-overlay">
      <div class="modal">
        <h3>Edit Node</h3>
        <input v-model="editForm.title_en" placeholder="Title (EN)" />
        <input v-model="editForm.title_sw" placeholder="Title (SW)" />
        <textarea v-model="editForm.content_en" placeholder="Content (EN)" />
        <textarea v-model="editForm.content_sw" placeholder="Content (SW)" />
        <div class="modal-actions">
          <button @click="submitEdit">Save</button>
          <button class="cancel" @click="showEdit = false">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <div v-if="showAdd" class="modal-overlay">
      <div class="modal">
        <h3>Add Subtopic</h3>
        <input v-model="addForm.title_en" placeholder="Title (EN)" />
        <input v-model="addForm.title_sw" placeholder="Title (SW)" />
        <textarea v-model="addForm.content_en" placeholder="Content (EN)" />
        <textarea v-model="addForm.content_sw" placeholder="Content (SW)" />
        <div class="modal-actions">
          <button @click="submitAdd">Add</button>
          <button class="cancel" @click="showAdd = false">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDelete" class="modal-overlay">
      <div class="modal">
        <h3>Confirm Delete</h3>
        <p>Are you sure you want to delete "<strong>{{ node.title_en }}</strong>"?</p>
        <div class="modal-actions">
          <button @click="submitDelete" class="danger">Yes, Delete</button>
          <button class="cancel" @click="showDelete = false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../services/api'
import NodeItem from './NodeItem.vue'

const props = defineProps({ node: Object })
const emit = defineEmits(['refresh'])

const expanded = ref(false)
const showEdit = ref(false)
const showAdd = ref(false)
const showDelete = ref(false)

const editForm = ref({
  title_en: '',
  title_sw: '',
  content_en: '',
  content_sw: ''
})

const addForm = ref({
  title_en: '',
  title_sw: '',
  content_en: '',
  content_sw: ''
})

const toggleExpanded = () => {
  expanded.value = !expanded.value
}

const submitEdit = async () => {
  await axios.put(`/api/admin/update/content-nodes/${props.node.id}/`, { ...editForm.value })
  showEdit.value = false
  emit('refresh')
}

const submitAdd = async () => {
  await axios.post('/api/admin/create/content-nodes/', {
    ...addForm.value,
    parent: props.node.id,
    node_type: props.node.node_type
  })
  showAdd.value = false
  emit('refresh')
}

const submitDelete = async () => {
  await axios.delete(`/api/admin/delete/content-nodes/${props.node.id}/`)
  showDelete.value = false
  emit('refresh')
}

onMounted(() => {
  editForm.value = {
    title_en: props.node.title_en,
    title_sw: props.node.title_sw,
    content_en: props.node.content_en || '',
    content_sw: props.node.content_sw || ''
  }
})
</script>

<style scoped>
.node-item {
  margin-left: 1rem;
  padding: 1rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 1rem;
  transition: 0.3s;
}

.node-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.node-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.node-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 0.5rem;
}
button {
    font-size: 14px;
  padding: 0.3rem 0.7rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background: var(--primary-red);
  color: #fff;
}
.node-toolbar button {
  font-size: 14px;
  padding: 0.3rem 0.7rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background: var(--primary-red);
  color: #fff;
}

.node-body {
  padding-left: 1rem;
  margin-top: 0.5rem;
  border-left: 2px dashed #f4bebe;
}

.content-block {
  margin-bottom: 0.5rem;
  background: #f9f9f9;
  padding: 0.5rem;
  border-radius: 8px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal {
  background: linear-gradient(to bottom right, #ffffff, #ffe6e6);
  padding: 1.5rem;
  border-radius: 10px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.modal input,
.modal textarea {
  width: 100%;
  margin-bottom: 0.8rem;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 14px;
}
.modal input:focus,
.modal textarea:focus {
    outline: none;
    border: 1px solid var(--primary-red); 
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

.modal-actions .cancel {
  background: #ccc;
}

.modal-actions .danger {
  background: red;
  color: white;
}
</style>
