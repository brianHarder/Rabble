import { createApp } from 'vue'
import SubrabbleDetail from '../pages/SubrabbleDetail.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(SubrabbleDetail, { pageData }).mount('#app')
