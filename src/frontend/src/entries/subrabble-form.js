import { createApp } from 'vue'
import SubrabbleForm from '../pages/SubrabbleForm.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(SubrabbleForm, { pageData }).mount('#app')
