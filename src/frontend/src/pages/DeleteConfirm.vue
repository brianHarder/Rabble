<template>
  <div class="text-center mt-5">
    <h2>{{ pageData.heading }}</h2>
    <div v-if="pageData.details" class="mt-4">
      <p v-for="(detail, i) in pageData.details" :key="i" v-html="detail"></p>
    </div>
    <form method="post" class="mt-4 d-inline-block">
      <input type="hidden" name="csrfmiddlewaretoken" :value="pageData.csrf_token" />
      <div class="d-flex justify-content-center gap-3">
        <button type="submit" class="btn btn-danger">{{ pageData.confirm_label || 'Delete' }}</button>
        <a :href="pageData.cancel_url" class="btn btn-secondary">Cancel</a>
      </div>
    </form>
  </div>
</template>

<script setup>
defineProps({
  pageData: { type: Object, default: () => ({}) },
})
</script>
