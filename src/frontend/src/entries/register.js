import { createApp } from 'vue'
import RegisterPage from '../pages/RegisterPage.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(RegisterPage, { pageData }).mount('#app')
