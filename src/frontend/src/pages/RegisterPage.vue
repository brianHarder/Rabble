<template>
  <div class="d-flex justify-content-center align-items-center" style="min-height: 60vh;">
    <div class="card shadow-sm p-4" style="width: 100%; max-width: 400px;">
      <div class="card-body">
        <h2 class="card-title text-center mb-4 text-rabble">Create an Account</h2>
        <form method="post" novalidate class="needs-validation" enctype="multipart/form-data">
          <input type="hidden" name="csrfmiddlewaretoken" :value="pageData.csrf_token" />

          <div v-if="pageData.form.non_field_errors.length" class="alert alert-danger mb-4">
            <span v-for="(err, i) in pageData.form.non_field_errors" :key="i">{{ err }}</span>
          </div>

          <div class="mb-4 text-center">
            <div class="profile-pic-container mb-3 mx-auto">
              <img :src="pageData.default_profile_pic" alt="Default profile picture" class="profile-pic-large" />
            </div>
            <div class="mb-3">
              <label for="id_profile_picture" class="form-label">Profile Picture (Optional)</label>
              <input
                type="file"
                name="profile_picture"
                id="id_profile_picture"
                class="form-control"
                accept="image/*"
              />
              <div v-if="fieldErrors('profile_picture')" class="text-danger small mt-1">
                {{ fieldErrors('profile_picture') }}
              </div>
            </div>
          </div>

          <div v-for="name in ['username', 'email', 'first_name', 'last_name']" :key="name" class="mb-3">
            <label :for="'id_' + name" class="form-label">{{ fieldLabel(name) }}</label>
            <input
              :type="fieldType(name)"
              :name="name"
              :id="'id_' + name"
              class="form-control rabble-input"
              :placeholder="fieldPlaceholder(name)"
              :value="fieldValue(name)"
            />
            <div v-if="fieldErrors(name)" class="text-danger small mt-1">
              {{ fieldErrors(name) }}
            </div>
          </div>

          <div v-for="name in ['password1', 'password2']" :key="name" class="mb-3">
            <label :for="'id_' + name" class="form-label">{{ fieldLabel(name) }}</label>
            <PasswordField
              :name="name"
              :id="'id_' + name"
              :placeholder="name === 'password1' ? 'Enter your password' : 'Confirm your password'"
            />
            <div v-if="fieldErrors(name)" class="text-danger small mt-1">
              {{ fieldErrors(name) }}
            </div>
            <small v-if="fieldHelpText(name)" class="form-text text-muted" v-html="fieldHelpText(name)"></small>
          </div>

          <button type="submit" class="btn btn-login w-100">Create Account</button>
        </form>
        <div class="text-center mt-3">
          <p class="mb-0">Already have an account? <a :href="pageData.login_url" class="text-rabble">Log in</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import PasswordField from '../components/PasswordField.vue'

const props = defineProps({
  pageData: { type: Object, default: () => ({}) },
})

const fields = props.pageData.form?.fields || {}

function fieldLabel(name) {
  return fields[name]?.label || name.replace('_', ' ')
}

function fieldType(name) {
  return fields[name]?.type || 'text'
}

function fieldPlaceholder(name) {
  return fields[name]?.placeholder || ''
}

function fieldValue(name) {
  return fields[name]?.value || ''
}

function fieldErrors(name) {
  const errs = fields[name]?.errors || []
  return errs.length ? errs.join(', ') : ''
}

function fieldHelpText(name) {
  return fields[name]?.help_text || ''
}
</script>
