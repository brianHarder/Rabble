<template>
  <div class="mb-4 d-flex justify-content-between align-items-center">
    <a :href="pageData.back_url" class="text-decoration-none text-muted">
      &larr; Back to {{ pageData.rabble_community_id }}
    </a>
  </div>

  <div class="d-flex justify-content-between align-items-center mb-2">
    <h1>!{{ pageData.subrabble.subrabble_community_id }} &mdash; {{ pageData.subrabble.subrabble_name }}</h1>
    <div v-if="pageData.is_owner" class="d-flex gap-2">
      <a :href="pageData.edit_url" class="btn btn-outline-secondary btn-sm">Edit Rabble</a>
      <a :href="pageData.delete_url" class="btn btn-outline-danger btn-sm">Delete Rabble</a>
    </div>
  </div>

  <p class="text-muted mb-4">{{ pageData.subrabble.description }}</p>

  <div class="d-flex justify-content-end mb-4">
    <a :href="pageData.new_post_url" class="btn btn-login">+ New Post</a>
  </div>

  <KnowledgeGraph :data="pageData.posts_with_relationships" />
</template>

<script setup>
import KnowledgeGraph from '../components/KnowledgeGraph.vue'

defineProps({
  pageData: { type: Object, default: () => ({}) },
})
</script>
