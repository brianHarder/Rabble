import { createApp } from 'vue'
import ProfilePage from '../pages/ProfilePage.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(ProfilePage, { pageData }).mount('#app')
