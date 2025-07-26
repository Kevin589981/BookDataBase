import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
	plugins: [
  		vue(),
    	vueDevTools(),
    ],
  	server: {
		host: '0.0.0.0',
		hmr: true,
		proxy: {
			// 配置代理，将/api开头的请求转发到后端服务器
			'/api': {
				target: 'http://localhost:8000',
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, ''),
			},
		},
		https: false,
  	},
  	resolve: {
    	alias: {
    	'@': fileURLToPath(new URL('./src', import.meta.url))
    	},
  	},
	  build: {
		outDir: 'dist', // 输出目录
		assetsDir: 'assets', // 静态资源目录
	  },
	  base: './', // 设置为相对路径，确保在Electron中正确加载
})
