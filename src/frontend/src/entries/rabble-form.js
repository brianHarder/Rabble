import { createApp } from 'vue'
import RabbleForm from '../pages/RabbleForm.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(RabbleForm, { pageData }).mount('#app')
