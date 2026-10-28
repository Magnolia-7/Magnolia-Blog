<template>
  <div class="app-shell" :style="{ '--manga-background': `url(${JSON.stringify(heroImage)})` }">
    <header class="site-header"><div class="header-inner"><RouterLink to="/" class="brand-avatar" aria-label="主页"><img :src="avatar" alt="山治头像" /></RouterLink><nav class="nav-links" aria-label="主导航"><RouterLink v-for="item in navItems" :key="item.to" :to="item.to">{{ item.label }}</RouterLink></nav></div></header>
    <main class="main-content"><RouterView /></main>
    <footer class="site-footer"><span class="comic">MAGNOLIA</span><div class="footer-links"><RouterLink to="/treelife/privacy">TreeLife 隐私政策</RouterLink><RouterLink to="/treelife/support">TreeLife 技术支持</RouterLink><a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">闽ICP备2026014322号-1</a><a href="https://beian.mps.gov.cn/#/query/webSearch?code=35082302000285" target="_blank" rel="noopener noreferrer">闽公网安备35082302000285号</a></div></footer>
  </div>
</template>
<script setup>
import { onMounted } from 'vue';
import { useSite, loadSite } from './composables/site';
const { avatar, heroImage } = useSite();
const navItems = [{ to: '/', label: '主页' }, { to: '/about', label: '关于' }, { to: '/records', label: '记录' }, { to: '/library', label: '图书馆' }, { to: '/friends', label: '友链' }, { to: '/guestbook', label: '留言' }, { to: '/search', label: '搜索' }];
onMounted(() => loadSite());
</script>
