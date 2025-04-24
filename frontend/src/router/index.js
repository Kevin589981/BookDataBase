import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import DashboardView from '@/views/DashboardView.vue'
import api from '@/utils/api'
// 添加路由守卫，检查用户是否已登录
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/dashboard',
            name: 'dashboard',
            component: DashboardView,
            meta: { requiresAuth: true } // 需要登录才能访问
        },
        {
            path: '/',
            name: 'home',
            component: HomeView,
            // 移除 requiresAuth，让欢迎页可以不登录访问
        },
        // 删除 about 路由
        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/LoginView.vue'),
        },
        {
            path: '/users',
            name: 'users',
            component: () => import('@/views/UsersView.vue'),
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    name: 'user-profile',
                    component: () => import('@/views/UsersView.vue'),
                    props: { defaultTab: 'profile' }
                },
                {
                    path: 'manage',
                    name: 'user-manage',
                    component: () => import('@/views/UsersView.vue'),
                    props: { defaultTab: 'users' },
                    meta: { requiresAdmin: true }
                }
            ]
        },
        {
            path: '/books',
            name: 'books',
            component: () => import('@/views/BooksView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/purchase',
            name: 'purchase',
            component: () => import('@/views/PurchaseView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/sale',
            name: 'sale',
            component: () => import('@/views/SaleView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/bills',
            name: 'bills',
            component: () => import('@/views/BillsView.vue'),
            meta: { requiresAuth: true }
        },
        // {
        //     path: '/profile',
        //     name: 'profile',
        //     component: () => import('@/views/ProfileView.vue'),
        //     meta: { requiresAuth: true }
        // },
        {
            path: '/api/login',  // 添加一个重定向路由，将/api/login重定向到/login
            redirect: '/login'
        }
    ],
})

// 添加全局前置守卫
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('token') // 检查是否有token
    
    // 检查token是否过期
    const tokenExpiration = localStorage.getItem('tokenExpiration')
    const isTokenExpired = tokenExpiration && new Date(tokenExpiration) < new Date()
    
    // 如果token过期，清除本地存储
    if (isTokenExpired) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('tokenExpiration')
    }
    
    if (to.meta.requiresAuth && (!isAuthenticated || isTokenExpired)) {
        // 需要登录但未认证或token已过期，跳转到登录页
        next({ name: 'login' })
    } else if (to.meta.requiresAdmin) {
        // 检查是否为管理员
        const userInfo = localStorage.getItem('user')
        if (userInfo) {
            const user = JSON.parse(userInfo)
            if (user.isSuperAdmin) {
                next() // 是管理员，放行
            } else {
                next({ name: 'dashboard' }) // 不是管理员，跳转到仪表盘
            }
        } else {
            next({ name: 'login' }) // 没有用户信息，跳转到登录页
        }
    } else {
        next() // 放行
    }
})

export default router
