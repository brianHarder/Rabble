<template>
  <div class="mb-4 d-flex justify-content-between align-items-center">
    <a :href="pageData.back_url" class="text-decoration-none text-muted">
      &larr; Back to !{{ pageData.subrabble_community_id }} &mdash; {{ pageData.subrabble_name }}
    </a>
  </div>

  <div class="mb-4">
    <h2>{{ pageData.post.title }}</h2>
    <p class="text-muted">
      By {{ pageData.post.anonymous ? 'anonymous' : pageData.post.username }}
    </p>
    <p>{{ pageData.post.body }}</p>

    <div class="d-flex justify-content-between align-items-center gap-3 mt-4">
      <div class="d-flex align-items-center gap-3">
        <LikeButton
          id="like-btn"
          :like-url="pageData.post.like_url"
          :username="pageData.username"
          :initial-liked="pageData.post.liked"
          :initial-count="pageData.post.like_count"
        />
        <span>&#x1F4AC; {{ pageData.post.comment_count }}</span>
      </div>
      <div v-if="pageData.post.is_owner" class="d-flex align-items-center gap-3 ms-auto">
        <a :href="pageData.post.edit_url" class="btn btn-outline-secondary btn-sm">Edit Post</a>
        <a :href="pageData.post.delete_url" class="btn btn-outline-danger btn-sm">Delete Post</a>
      </div>
    </div>
  </div>

  <hr />

  <div class="d-flex justify-content-between align-items-center mb-2">
    <h4>Comments</h4>
    <a :href="pageData.new_comment_url" class="btn btn-outline-secondary btn-sm">New Comment</a>
  </div>

  <ul v-if="pageData.comments?.length" class="list-group mb-3">
    <CommentItem
      v-for="comment in pageData.comments"
      :key="comment.pk"
      :comment="comment"
      :username="pageData.username"
    />
  </ul>
  <p v-else>No comments yet. Be the first to comment!</p>
</template>

<script setup>
import LikeButton from '../components/LikeButton.vue'
import CommentItem from '../components/CommentItem.vue'

defineProps({
  pageData: { type: Object, default: () => ({}) },
})
</script>
