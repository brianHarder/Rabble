<template>
  <div class="d-flex justify-content-center align-items-center" style="min-height: 60vh;">
    <div class="card shadow-sm p-4" style="width: 100%; max-width: 400px;">
      <div class="card-body">
        <h2 class="card-title text-center mb-4 text-rabble">Reset Password</h2>
        <p class="text-center mb-4">
          Enter a valid email address and username combination to reset your password.
        </p>

        <form method="post" class="needs-validation">
          <input type="hidden" name="csrfmiddlewaretoken" :value="pageData.csrf_token" />

          <div v-if="pageData.form.non_field_errors.length" class="alert alert-danger mb-4">
            <span v-for="(err, i) in pageData.form.non_field_errors" :key="i">{{ err }}</span>
          </div>

          <div v-for="(field, name) in pageData.form.fields" :key="name" class="mb-3">
            <label :for="'id_' + name" class="form-label">{{ field.label }}</label>
            <PasswordField
              v-if="field.type === 'password'"
              :name="name"
              :id="'id_' + name"
              :placeholder="field.placeholder"
              :model-value="field.value"
            />
            <input
              v-else
              :type="field.type"
              :name="name"
              :id="'id_' + name"
              class="form-control"
              :placeholder="field.placeholder"
              :value="field.value"
            />
            <div v-if="field.errors.length" class="text-danger small mt-1">
              {{ field.errors.join(', ') }}
            </div>
          </div>

          <button type="submit" class="btn btn-login w-100">Reset Password</button>
        </form>

        <div class="text-center mt-3">
          <p class="mb-0">
            <a :href="pageData.login_url" class="text-rabble text-decoration-none">Back to Login</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import PasswordField from '../components/PasswordField.vue'

defineProps({
  pageData: { type: Object, default: () => ({}) },
})
</script>

<style scoped>
.main-content {
  background-color: white;
  min-height: calc(100vh - 72px);
}
</style>
