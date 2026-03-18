import { createApp } from 'vue'
import LoginPage from '../pages/LoginPage.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(LoginPage, { pageData }).mount('#app')
