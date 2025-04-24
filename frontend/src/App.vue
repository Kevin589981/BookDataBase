<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div class="app-container">
    <!-- 背景图层 -->
    <div class="bg-overlay"></div>
    
    <!-- 原有内容 -->
    <!-- <header>
      <img alt="Vue logo" class="logo" src="@/assets/booklogo.png" width="125" height="125" />
      <div class="wrapper">
        <HelloWorld msg="图书管理系统" />
        <nav>
          <RouterLink to="/home">欢迎页</RouterLink>
          <RouterLink to="/">系统首页</RouterLink>
        </nav>
      </div>
    </header> -->
    <!-- <div class="content-wrapper"> -->
      <RouterView />
    <!-- </div> -->
  </div>
</template>

<style scoped>
.app-container {
  position: relative;
  min-height: 100vh;
  background-color: transparent; /* 添加此行使容器透明 */
}

.bg-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/img.png') no-repeat center center;
  background-size: cover;
  opacity: 0.4;
  z-index: -1;
}

/* 确保RouterView内容区域也是透明的 */
:deep(.content-wrapper) {
  background-color: transparent;
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.content-wrapper {
  width: 100%;
  box-sizing: border-box;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
