import { createApp } from 'vue'
import CommentForm from '../pages/CommentForm.vue'

const el = document.getElementById('page-data')
const pageData = el ? JSON.parse(el.textContent) : {}
createApp(CommentForm, { pageData }).mount('#app')
