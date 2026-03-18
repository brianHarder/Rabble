<template>
  <div class="d-flex justify-content-center align-items-center" style="min-height: 60vh;">
    <div class="decoration-circle circle-1"></div>
    <div class="decoration-circle circle-2"></div>
    <div class="decoration-circle circle-3"></div>

    <div class="login-container">
      <div class="card login-card p-4" style="width: 100%; max-width: 450px;">
        <div class="card-body">
          <h2 class="login-title text-center">Welcome Back</h2>
          <p class="login-subtitle text-center">Sign in to continue to Rabble</p>

          <form method="post" class="needs-validation" id="login-form">
            <input type="hidden" name="csrfmiddlewaretoken" :value="pageData.csrf_token" />

            <div v-if="pageData.form.non_field_errors.length" class="alert alert-danger mb-4">
              <span v-for="(err, i) in pageData.form.non_field_errors" :key="i">{{ err }}</span>
            </div>

            <div class="mb-4">
              <label for="id_username" class="form-label">Username</label>
              <input
                type="text"
                name="username"
                id="id_username"
                class="form-control"
                placeholder="Enter your username"
                required
                v-model="username"
              />
              <div v-if="pageData.form.fields.username?.errors?.length" class="text-danger small mt-1">
                {{ pageData.form.fields.username.errors.join(', ') }}
              </div>
            </div>

            <div class="mb-3">
              <label for="id_password" class="form-label">Password</label>
              <div class="password-field-container">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  name="password"
                  id="id_password"
                  class="form-control"
                  placeholder="Enter your password"
                  required
                  v-model="password"
                />
                <button type="button" class="password-toggle" @click="showPassword = !showPassword">
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
              <div v-if="pageData.form.fields.password?.errors?.length" class="text-danger small mt-1">
                {{ pageData.form.fields.password.errors.join(', ') }}
              </div>
            </div>

            <div class="mb-4 text-end">
              <a :href="pageData.forgot_password_url" class="text-rabble text-decoration-none">Forgot Password?</a>
            </div>

            <button type="submit" class="btn btn-login w-100">Sign In</button>
          </form>

          <div class="text-center mt-4">
            <p class="mb-0">Don't have an account? <a :href="pageData.register_url" class="text-rabble">Create one</a></p>
          </div>

          <div class="welcome-message mt-4">
            <h3>Join the Conversation</h3>
            <p>Connect with communities and share your ideas</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <button class="guest-login-btn" @click="handleGuestLogin">
    <i class="bi bi-person-fill me-1"></i> Continue as Guest
  </button>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  pageData: { type: Object, default: () => ({}) },
})

const username = ref('')
const password = ref('')
const showPassword = ref(false)

function handleGuestLogin() {
  username.value = 'guest'
  password.value = 'xgU23*lY'
  const form = document.getElementById('login-form')
  setTimeout(() => form.submit(), 0)
}
</script>

<style scoped>
.login-container {
  position: relative;
  z-index: 1;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.login-title {
  font-family: 'Bebas Neue', cursive;
  font-size: 2.5rem;
  color: var(--rabble-primary);
  margin-bottom: 1.5rem;
}

.login-subtitle {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.form-control {
  border-radius: 10px;
  padding: 12px;
  border: 2px solid #eee;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: var(--rabble-primary);
  box-shadow: 0 0 0 0.2rem rgba(217, 56, 30, 0.15);
}

.btn-login {
  padding: 12px;
  font-size: 1.1rem;
  border-radius: 10px;
  margin-top: 1rem;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, var(--rabble-primary), var(--rabble-accent));
  opacity: 0.1;
}

.circle-1 { width: 300px; height: 300px; top: -100px; right: -100px; }
.circle-2 { width: 200px; height: 200px; bottom: -50px; left: -50px; }
.circle-3 { width: 150px; height: 150px; top: 50%; left: 10%; }

.password-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
}

.password-field-container {
  position: relative;
}

.welcome-message {
  background: linear-gradient(45deg, var(--rabble-primary), var(--rabble-accent));
  color: white;
  padding: 1rem;
  border-radius: 10px;
  margin-top: 2rem;
  text-align: center;
}

.welcome-message h3 { margin: 0; font-size: 1.2rem; font-weight: 500; }
.welcome-message p { margin: 0.5rem 0 0; opacity: 0.9; font-size: 0.9rem; }

.guest-login-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: linear-gradient(45deg, var(--rabble-primary), var(--rabble-accent));
  color: white;
  border: none;
  border-radius: 25px;
  padding: 12px 25px;
  font-size: 1.1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 1000;
}

.guest-login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  color: white;
}
</style>
