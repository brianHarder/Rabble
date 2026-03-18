<template>
  <button
    class="btn btn-light p-0 border-0"
    :class="{ liked: isLiked }"
    :disabled="!username"
    :title="!username ? 'Log in to like' : ''"
    @click="toggle"
  >
    <i class="bi bi-hand-thumbs-up-fill"></i>
    <span>{{ count }}</span>
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { apiFetch } from '../api.js'

const props = defineProps({
  likeUrl: { type: String, required: true },
  username: { type: String, default: '' },
  initialLiked: { type: Boolean, default: false },
  initialCount: { type: Number, default: 0 },
})

const isLiked = ref(props.initialLiked)
const count = ref(props.initialCount)

async function toggle() {
  if (!props.username) return alert('Log in to like posts')
  try {
    const data = await apiFetch(props.likeUrl, {
      method: 'POST',
      body: JSON.stringify({ user: props.username }),
    })
    count.value = data.like_count
    isLiked.value = data.liked
  } catch {
    alert('Sorry, could not toggle like.')
  }
}
</script>
