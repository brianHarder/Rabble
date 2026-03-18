import { createApp } from 'vue'
import IndexPage from '../pages/IndexPage.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(IndexPage, { pageData }).mount('#app')
