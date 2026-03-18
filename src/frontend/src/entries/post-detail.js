import { createApp } from 'vue'
import PostDetail from '../pages/PostDetail.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(PostDetail, { pageData }).mount('#app')
