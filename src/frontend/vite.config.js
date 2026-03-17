import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

const entries = {
  'index': resolve(__dirname, 'src/entries/index.js'),
  'rabble-detail': resolve(__dirname, 'src/entries/rabble-detail.js'),
  'rabble-form': resolve(__dirname, 'src/entries/rabble-form.js'),
  'subrabble-detail': resolve(__dirname, 'src/entries/subrabble-detail.js'),
  'subrabble-form': resolve(__dirname, 'src/entries/subrabble-form.js'),
  'post-detail': resolve(__dirname, 'src/entries/post-detail.js'),
  'post-form': resolve(__dirname, 'src/entries/post-form.js'),
  'comment-form': resolve(__dirname, 'src/entries/comment-form.js'),
  'delete-confirm': resolve(__dirname, 'src/entries/delete-confirm.js'),
  'profile': resolve(__dirname, 'src/entries/profile.js'),
  'login': resolve(__dirname, 'src/entries/login.js'),
  'register': resolve(__dirname, 'src/entries/register.js'),
  'forgot-password': resolve(__dirname, 'src/entries/forgot-password.js'),
}

export default defineConfig({
  plugins: [vue()],
  base: '/static/dist/',
  build: {
    outDir: resolve(__dirname, '..', 'static', 'dist'),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: entries,
    },
  },
  server: {
    host: 'localhost',
    port: 5173,
    strictPort: true,
    origin: 'http://localhost:5173',
  },
})
