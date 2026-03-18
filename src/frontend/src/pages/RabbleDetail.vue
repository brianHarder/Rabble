<template>
  <div class="mb-4 d-flex justify-content-between align-items-center">
    <a :href="pageData.index_url" class="text-decoration-none text-muted">
      &larr; Back to homepage
    </a>
  </div>

  <div class="d-flex justify-content-between align-items-center mb-3">
    <div>
      <h2>{{ pageData.rabble.community_id }}</h2>
      <p class="text-muted">{{ pageData.rabble.description }}</p>
    </div>
    <div class="d-flex flex-column gap-2">
      <div v-if="pageData.is_owner" class="d-flex gap-2">
        <a :href="pageData.edit_url" class="btn btn-outline-secondary">Edit Community</a>
        <a :href="pageData.delete_url" class="btn btn-outline-danger">Delete Community</a>
      </div>
      <a :href="pageData.create_subrabble_url" class="btn btn-primary">New Rabble</a>
    </div>
  </div>

  <SubrabbleCarousel :subrabbles="pageData.subrabbles" />
</template>

<script setup>
import SubrabbleCarousel from '../components/SubrabbleCarousel.vue'

defineProps({
  pageData: { type: Object, default: () => ({}) },
})
</script>
