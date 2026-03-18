import { createApp } from 'vue'
import ForgotPassword from '../pages/ForgotPassword.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(ForgotPassword, { pageData }).mount('#app')
