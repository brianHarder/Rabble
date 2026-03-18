<template>
  <div class="mb-4 d-flex justify-content-between align-items-center">
    <a :href="pageData.index_url" class="text-decoration-none text-muted">
      &larr; Back to Rabble
    </a>
  </div>
  <div class="container py-5">
    <div class="row">
      <div class="col-md-8 mx-auto">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h3 class="mb-0">Profile Settings</h3>
          </div>
          <div class="card-body">
            <div v-if="pageData.messages?.length">
              <div
                v-for="(msg, i) in pageData.messages"
                :key="i"
                :class="'alert alert-' + msg.tags + ' alert-dismissible fade show'"
                role="alert"
              >
                {{ msg.text }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            </div>

            <form method="post" class="needs-validation" novalidate enctype="multipart/form-data">
              <input type="hidden" name="csrfmiddlewaretoken" :value="pageData.csrf_token" />

              <div class="mb-4 text-center">
                <div class="profile-pic-container mb-3">
                  <img :src="pageData.profile_picture_url" :alt="pageData.username + '\'s profile picture'" class="profile-pic-large" />
                </div>
                <div class="mb-3">
                  <label for="id_profile_picture" class="form-label">Profile Picture</label>
                  <div class="d-flex gap-2 align-items-center">
                    <div class="flex-grow-1">
                      <input
                        type="file"
                        name="profile_picture"
                        id="id_profile_picture"
                        class="form-control"
                        accept="image/*"
                      />
                    </div>
                    <button
                      v-if="!pageData.is_default_pic"
                      type="submit"
                      name="reset_profile_picture"
                      value="true"
                      class="btn btn-outline-secondary flex-shrink-0"
                    >
                      Reset to Default
                    </button>
                  </div>
                  <div v-if="fieldErrors('profile_picture')" class="invalid-feedback d-block">
                    {{ fieldErrors('profile_picture') }}
                  </div>
                </div>
              </div>

              <div class="mb-4">
                <h5 class="card-title mb-3">Personal Information</h5>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label for="id_first_name" class="form-label">First Name</label>
                    <input type="text" name="first_name" id="id_first_name" class="form-control" placeholder="Enter your first name" :value="fieldValue('first_name')" />
                    <div v-if="fieldErrors('first_name')" class="invalid-feedback d-block">{{ fieldErrors('first_name') }}</div>
                  </div>
                  <div class="col-md-6">
                    <label for="id_last_name" class="form-label">Last Name</label>
                    <input type="text" name="last_name" id="id_last_name" class="form-control" placeholder="Enter your last name" :value="fieldValue('last_name')" />
                    <div v-if="fieldErrors('last_name')" class="invalid-feedback d-block">{{ fieldErrors('last_name') }}</div>
                  </div>
                </div>
              </div>

              <div class="mb-4">
                <h5 class="card-title mb-3">Account Information</h5>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label for="id_username" class="form-label">Username</label>
                    <input type="text" name="username" id="id_username" class="form-control" placeholder="Enter your username" :value="fieldValue('username')" />
                    <div v-if="fieldErrors('username')" class="invalid-feedback d-block">{{ fieldErrors('username') }}</div>
                  </div>
                  <div class="col-md-6">
                    <label for="id_email" class="form-label">Email</label>
                    <input type="email" name="email" id="id_email" class="form-control" placeholder="Enter your email" :value="fieldValue('email')" />
                    <div v-if="fieldErrors('email')" class="invalid-feedback d-block">{{ fieldErrors('email') }}</div>
                  </div>
                </div>
              </div>

              <div class="mb-4">
                <h5 class="card-title mb-3">Change Password</h5>
                <div class="row g-3">
                  <div class="col-md-12">
                    <label for="id_current_password" class="form-label">Current Password</label>
                    <PasswordField name="current_password" id="id_current_password" placeholder="Enter current password to confirm changes" />
                    <div v-if="fieldErrors('current_password')" class="invalid-feedback d-block">{{ fieldErrors('current_password') }}</div>
                  </div>
                  <div class="col-md-6">
                    <label for="id_new_password" class="form-label">New Password</label>
                    <PasswordField name="new_password" id="id_new_password" placeholder="Enter new password" />
                    <div v-if="fieldErrors('new_password')" class="invalid-feedback d-block">{{ fieldErrors('new_password') }}</div>
                  </div>
                  <div class="col-md-6">
                    <label for="id_confirm_password" class="form-label">Confirm New Password</label>
                    <PasswordField name="confirm_password" id="id_confirm_password" placeholder="Confirm new password" />
                    <div v-if="fieldErrors('confirm_password')" class="invalid-feedback d-block">{{ fieldErrors('confirm_password') }}</div>
                  </div>
                </div>
              </div>

              <div v-if="pageData.form.non_field_errors.length" class="alert alert-danger">
                <span v-for="(err, i) in pageData.form.non_field_errors" :key="i">{{ err }}</span>
              </div>

              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">Save Changes</button>
              </div>
            </form>
          </div>
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

function fieldValue(name) {
  return fields[name]?.value || ''
}

function fieldErrors(name) {
  const errs = fields[name]?.errors || []
  return errs.length ? errs.join(', ') : ''
}
</script>
