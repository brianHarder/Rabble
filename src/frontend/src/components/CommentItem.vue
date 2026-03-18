<template>
  <li class="list-group-item">
    <div class="d-flex justify-content-between align-items-start">
      <div>
        <p>{{ comment.text }}</p>
        <div class="d-flex align-items-center gap-3">
          <small class="text-muted">
            By {{ comment.anonymous ? 'anonymous' : comment.username }}
          </small>
          <LikeButton
            class="comment-like-btn"
            :like-url="comment.likeUrl"
            :username="username"
            :initial-liked="comment.userHasLiked"
            :initial-count="comment.likeCount"
          />
          <DislikeButton
            class="comment-dislike-btn"
            :dislike-url="comment.dislikeUrl"
            :username="username"
            :initial-disliked="comment.userHasDisliked"
            :initial-count="comment.dislikeCount"
          />
        </div>
      </div>
      <div v-if="comment.isOwner" class="d-flex flex-column gap-1 ms-3">
        <a :href="comment.editUrl" class="btn btn-outline-secondary btn-sm">Edit</a>
        <a :href="comment.deleteUrl" class="btn btn-outline-secondary btn-sm">Delete</a>
      </div>
    </div>
  </li>
</template>

<script setup>
import LikeButton from './LikeButton.vue'
import DislikeButton from './DislikeButton.vue'

defineProps({
  comment: { type: Object, required: true },
  username: { type: String, default: '' },
})
</script>
