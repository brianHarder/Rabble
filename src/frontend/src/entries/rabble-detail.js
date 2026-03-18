import { createApp } from 'vue'
import RabbleDetail from '../pages/RabbleDetail.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(RabbleDetail, { pageData }).mount('#app')
