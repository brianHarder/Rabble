<template>
  <div class="mt-4">
    <h2>{{ pageData.form.is_edit ? 'Edit Rabble' : 'New Rabble' }}</h2>

    <form method="post" class="mt-3" @submit="handleSubmit">
      <input type="hidden" name="csrfmiddlewaretoken" :value="pageData.csrf_token" />

      <div v-if="nonFieldErrors.length" class="alert alert-danger">
        <span v-for="(err, i) in nonFieldErrors" :key="i">{{ err }}<br v-if="i < nonFieldErrors.length - 1" /></span>
      </div>

      <div class="mb-3">
        <label for="id_subrabble_community_id" class="form-label">Community ID</label>
        <input
          type="text"
          name="subrabble_community_id"
          id="id_subrabble_community_id"
          class="form-control"
          placeholder="Enter community ID (letters, numbers, and dashes only)…"
          pattern="[a-zA-Z0-9-]*"
          title="Community ID can only contain letters, numbers, and dashes"
          v-model="formData.subrabble_community_id"
        />
        <div v-if="errors.subrabble_community_id?.length" class="text-danger small mt-1">
          {{ errors.subrabble_community_id.join(', ') }}
        </div>
      </div>

      <div class="mb-3">
        <label for="id_subrabble_name" class="form-label">Name</label>
        <input
          type="text"
          name="subrabble_name"
          id="id_subrabble_name"
          class="form-control"
          placeholder="Enter Rabble name…"
          v-model="formData.subrabble_name"
        />
        <div v-if="errors.subrabble_name?.length" class="text-danger small mt-1">
          {{ errors.subrabble_name.join(', ') }}
        </div>
      </div>

      <div class="mb-3">
        <label for="id_description" class="form-label">Description</label>
        <textarea
          name="description"
          id="id_description"
          class="form-control"
          rows="4"
          placeholder="What is this Rabble about?"
          v-model="formData.description"
        ></textarea>
        <div v-if="errors.description?.length" class="text-danger small mt-1">
          {{ errors.description.join(', ') }}
        </div>
      </div>

      <div class="form-check mb-3">
        <input
          type="checkbox"
          name="allow_anonymous"
          id="id_allow_anonymous"
          class="form-check-input"
          v-model="formData.allow_anonymous"
        />
        <label for="id_allow_anonymous" class="form-check-label">Allow anonymous posts?</label>
      </div>

      <div class="form-check mb-4">
        <input
          type="checkbox"
          name="private"
          id="id_private"
          class="form-check-input"
          v-model="formData.private"
        />
        <label for="id_private" class="form-check-label">Private Rabble?</label>
      </div>

      <MemberSelect
        name="members"
        label="Members"
        :options="pageData.member_choices"
        v-model="formData.members"
        :visible="formData.private"
      />

      <button type="submit" class="btn btn-primary">
        {{ pageData.form.is_edit ? 'Save Changes' : 'Create Rabble' }}
      </button>
      <a :href="pageData.cancel_url" class="btn btn-secondary ms-2">Cancel</a>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { apiFetch } from '../api.js'
import MemberSelect from '../components/MemberSelect.vue'

const props = defineProps({
  pageData: { type: Object, default: () => ({}) },
})

const f = props.pageData.form?.fields || {}
const formData = reactive({
  subrabble_community_id: f.subrabble_community_id?.value || '',
  subrabble_name: f.subrabble_name?.value || '',
  description: f.description?.value || '',
  allow_anonymous: f.allow_anonymous?.value === true || f.allow_anonymous?.value === 'True',
  private: f.private?.value === true || f.private?.value === 'True',
  members: Array.isArray(f.members?.value) ? f.members.value.map(String) : [],
})

const errors = reactive({
  subrabble_community_id: f.subrabble_community_id?.errors || [],
  subrabble_name: f.subrabble_name?.errors || [],
  description: f.description?.errors || [],
})

const nonFieldErrors = ref([...(props.pageData.form?.non_field_errors || [])])

async function handleSubmit(e) {
  if (!props.pageData.form.is_edit) return

  e.preventDefault()
  nonFieldErrors.value = []

  const data = {
    subrabble_community_id: formData.subrabble_community_id,
    subrabble_name: formData.subrabble_name,
    description: formData.description,
    allow_anonymous: formData.allow_anonymous,
    private: formData.private,
  }
  if (formData.private) {
    data.members = formData.members
  }

  try {
    await apiFetch(props.pageData.edit_url, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
    let successUrl = props.pageData.success_url
    if (
      formData.subrabble_community_id &&
      formData.subrabble_community_id !== props.pageData.original_community_id
    ) {
      successUrl = successUrl.replace(
        props.pageData.original_community_id,
        formData.subrabble_community_id
      )
    }
    window.location.href = successUrl
  } catch (err) {
    if (err.data) {
      if (typeof err.data === 'object') {
        Object.entries(err.data).forEach(([field, msgs]) => {
          if (errors[field] !== undefined) {
            errors[field] = Array.isArray(msgs) ? msgs : [msgs]
          } else {
            nonFieldErrors.value.push(`${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
          }
        })
      }
    }
  }
}
</script>
