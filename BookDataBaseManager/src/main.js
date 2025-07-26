import './assets/main.css'

import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import api from '@/utils/api'
// import "@fortawesome/fontawesome-free/css/all.min.css";
import "font-awesome/css/font-awesome.min.css";
const app = createApp(App)
// const app=createApp()
// 将api实例添加到全局属性中
app.config.globalProperties.$api = api

app.use(router)

app.mount('#app')
