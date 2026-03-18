<template>
  <h2>
    {{ pageData.form.is_edit ? 'Edit Post' : 'New Post in !' + pageData.subrabble_community_id }}
  </h2>

  <form
    method="post"
    class="mt-4"
    @submit="handleSubmit"
  >
    <input type="hidden" name="csrfmiddlewaretoken" :value="pageData.csrf_token" />

    <div class="mb-3">
      <label for="id_title" class="form-label">Title</label>
      <input
        type="text"
        name="title"
        id="id_title"
        class="form-control"
        placeholder="Write your title here…"
        v-model="formData.title"
      />
      <div v-if="errors.title" class="text-danger small mt-1">
        {{ errors.title.join(', ') }}
      </div>
    </div>

    <div class="mb-3">
      <label for="id_body" class="form-label">Body</label>
      <textarea
        name="body"
        id="id_body"
        class="form-control"
        rows="5"
        placeholder="Write your post here…"
        v-model="formData.body"
      ></textarea>
      <div v-if="errors.body" class="text-danger small mt-1">
        {{ errors.body.join(', ') }}
      </div>
    </div>

    <div v-if="pageData.allow_anonymous" class="mb-3">
      <div class="form-check d-flex align-items-center">
        <input
          type="checkbox"
          name="anonymous"
          id="id_anonymous"
          class="form-check-input"
          v-model="formData.anonymous"
        />
        <label class="form-check-label ms-2" for="id_anonymous">Post anonymously</label>
      </div>
    </div>

    <button type="submit" class="btn btn-login">
      {{ pageData.form.is_edit ? 'Save Changes' : 'Create Post' }}
    </button>
    <a :href="pageData.cancel_url" class="btn btn-secondary ms-2">Cancel</a>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { apiFetch } from '../api.js'

const props = defineProps({
  pageData: { type: Object, default: () => ({}) },
})

const f = props.pageData.form?.fields || {}
const formData = reactive({
  title: f.title?.value || '',
  body: f.body?.value || '',
  anonymous: f.anonymous?.value === true || f.anonymous?.value === 'True',
})

const errors = reactive({
  title: f.title?.errors || [],
  body: f.body?.errors || [],
})

const serverErrors = ref([...(props.pageData.form?.non_field_errors || [])])

async function handleSubmit(e) {
  if (!props.pageData.form.is_edit) return

  e.preventDefault()
  try {
    await apiFetch(props.pageData.edit_url, {
      method: 'PATCH',
      body: JSON.stringify({
        title: formData.title,
        body: formData.body,
        anonymous: formData.anonymous,
      }),
    })
    window.location.href = props.pageData.success_url
  } catch (err) {
    if (err.data) {
      Object.keys(err.data).forEach((field) => {
        if (errors[field] !== undefined) {
          errors[field] = err.data[field]
        }
      })
    }
  }
}
</script>
