<template>
  <div class="email-preview">
    <h2 class="preview-title">{{ title }}</h2>
    <div class="preview-layout"><i>Layout: {{ layoutLabel }}</i></div>
    <div class="preview-content" v-html="renderedMarkdown"></div>
  </div>
</template>

<script>
import { marked } from 'marked'

export default {
  name: 'EmailPreview',
  props: {
    title: {
      type: String,
      default: 'Untitled Email'
    },
    layout: {
      type: String,
      default: 'default'
    },
    content: {
      type: String,
      default: ''
    }
  },
  computed: {
    layoutLabel() {
      return this.layout
        ? this.layout.charAt(0).toUpperCase() + this.layout.slice(1)
        : 'Default';
    },
    renderedMarkdown() {
      return marked(this.content || '');
    }
  }
}
</script>

<style scoped>
.email-preview {
  background: #ffffff;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  color: #203a43;
  margin-top: 2rem;
}

.preview-title {
  color: #2c5364;
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.preview-layout {
  font-size: 0.85rem;
  color: gray;
  margin-bottom: 1rem;
}

.preview-content {
  line-height: 1.6;
}
.preview-content h1,
.preview-content h2,
.preview-content h3 {
  margin-top: 1rem;
  color: #2c5364;
}
.preview-content blockquote {
  border-left: 4px solid #00c6ff;
  padding-left: 1rem;
  color: #555;
}
.preview-content ul {
  margin-left: 1.5rem;
}
</style>
