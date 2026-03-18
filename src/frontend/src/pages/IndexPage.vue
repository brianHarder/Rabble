<template>
  <div class="rabble-grid">
    <template v-if="visibleRabbles.length">
      <a
        v-for="(rabble, i) in visibleRabbles"
        :key="rabble.community_id"
        :href="rabble.url"
        :class="'rabble-card pattern-' + ((i % 10) + 1)"
      >
        <div :class="'geometric-pattern pattern-svg-' + ((i % 10) + 1)"></div>
        <div class="rabble-content">
          <h2 class="rabble-title">{{ rabble.community_id }}</h2>
          <p class="rabble-description">{{ rabble.description }}</p>
        </div>
      </a>
    </template>
    <div v-else class="no-rabbles">
      <h2>No communities yet</h2>
      <p>Create one to get started!</p>
    </div>
  </div>

  <a v-if="pageData.is_authenticated" :href="pageData.create_url" class="btn btn-primary new-rabble-btn">
    <i class="bi bi-plus-lg me-2"></i>New Community
  </a>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  pageData: { type: Object, default: () => ({}) },
})

const visibleRabbles = computed(() => {
  return (props.pageData.rabbles || []).filter(
    (r) => !r.private || r.is_member
  )
})
</script>
