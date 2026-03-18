import { createApp } from 'vue'
import PostForm from '../pages/PostForm.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(PostForm, { pageData }).mount('#app')
