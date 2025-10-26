import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// compose のサービス名 backend へ
const target = process.env.VITE_PROXY_TARGET || 'http://backend:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target,
        changeOrigin: true,
      },
    },
  },
})
