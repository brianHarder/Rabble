import { createApp } from 'vue'
import DeleteConfirm from '../pages/DeleteConfirm.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(DeleteConfirm, { pageData }).mount('#app')
