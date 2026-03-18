<template>
  <button
    class="btn btn-light p-0 border-0"
    :class="{ disliked: isDisliked }"
    :disabled="!username"
    :title="!username ? 'Log in to dislike' : ''"
    @click="toggle"
  >
    <i class="bi bi-hand-thumbs-down-fill"></i>
    <span>{{ count }}</span>
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { apiFetch } from '../api.js'

const props = defineProps({
  dislikeUrl: { type: String, required: true },
  username: { type: String, default: '' },
  initialDisliked: { type: Boolean, default: false },
  initialCount: { type: Number, default: 0 },
})

const isDisliked = ref(props.initialDisliked)
const count = ref(props.initialCount)

async function toggle() {
  if (!props.username) return alert('Log in to dislike comments')
  try {
    const data = await apiFetch(props.dislikeUrl, {
      method: 'POST',
      body: JSON.stringify({ user: props.username }),
    })
    count.value = data.dislike_count
    isDisliked.value = data.disliked
  } catch {
    alert('Sorry, could not toggle dislike.')
  }
}
</script>
