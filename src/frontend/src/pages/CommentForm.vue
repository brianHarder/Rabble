<template>
  <h2>
    {{ pageData.form.is_edit ? 'Edit Comment' : 'New Comment on "' + pageData.post_title + '"' }}
  </h2>

  <form
    method="post"
    class="mt-4"
    @submit="handleSubmit"
  >
    <input type="hidden" name="csrfmiddlewaretoken" :value="pageData.csrf_token" />

    <div class="mb-3">
      <label for="id_text" class="form-label">Text</label>
      <textarea
        name="text"
        id="id_text"
        class="form-control"
        rows="5"
        placeholder="Write your comment here…"
        v-model="formData.text"
      ></textarea>
      <div v-if="errors.text" class="text-danger small mt-1">
        {{ errors.text.join(', ') }}
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
      {{ pageData.form.is_edit ? 'Save Changes' : 'Add Comment' }}
    </button>
    <a :href="pageData.cancel_url" class="btn btn-secondary ms-2">Cancel</a>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { apiFetch } from '../api.js'

const props = defineProps({
  pageData: { type: Object, default: () => ({}) },
})

const f = props.pageData.form?.fields || {}
const formData = reactive({
  text: f.text?.value || '',
  anonymous: f.anonymous?.value === true || f.anonymous?.value === 'True',
})

const errors = reactive({
  text: f.text?.errors || [],
})

async function handleSubmit(e) {
  if (!props.pageData.form.is_edit) return

  e.preventDefault()
  try {
    await apiFetch(props.pageData.edit_url, {
      method: 'PATCH',
      body: JSON.stringify({
        text: formData.text,
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
