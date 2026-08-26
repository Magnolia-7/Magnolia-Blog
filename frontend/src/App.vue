<template>
  <div class="app-shell">
    <header class="site-header">
      <div class="header-inner">
        <RouterLink to="/" class="brand" @click="menuOpen = false">
          <span class="brand-mark">M</span>
          <span class="brand-copy">
            <strong>Magnolia Nook</strong>
            <small>个人数字花园</small>
          </span>
        </RouterLink>

        <button
          class="menu-button"
          type="button"
          :aria-expanded="menuOpen"
          aria-label="打开导航菜单"
          @click="menuOpen = !menuOpen"
        >
          <span></span><span></span>
        </button>

        <nav :class="['nav-links', { open: menuOpen }]" aria-label="主导航">
          <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" @click="menuOpen = false">
            {{ item.label }}
          </RouterLink>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <RouterView />
    </main>

    <footer class="site-footer">
      <div class="footer-flower">✦</div>
      <p>愿这里像一朵慢慢盛开的白玉兰，安静记录每一次成长。</p>
      <div class="footer-links">
        <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">闽ICP备2026014322号-1</a>
        <a href="https://beian.mps.gov.cn/#/query/webSearch?code=35082302000285" target="_blank" rel="noopener noreferrer">
          闽公网安备35082302000285号
        </a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";

const menuOpen = ref(false);
const navItems = [
  { to: "/", label: "主页" },
  { to: "/about", label: "关于" },
  { to: "/records", label: "记录" },
  { to: "/library", label: "图书馆" },
  { to: "/guestbook", label: "留言" },
  { to: "/changelog", label: "更新日志" },
  { to: "/search", label: "搜索" },
];
</script>

<style scoped>
.app-shell { min-height: 100vh; display: flex; flex-direction: column; }
.site-header { position: fixed; inset: 0 0 auto; z-index: 50; border-bottom: 1px solid var(--line); background: color-mix(in srgb, var(--paper) 88%, transparent); backdrop-filter: blur(18px); }
.header-inner { width: min(1240px, calc(100% - 40px)); height: 68px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 28px; }
.brand { display: inline-flex; align-items: center; gap: 11px; text-decoration: none; flex: 0 0 auto; }
.brand-mark { width: 36px; height: 36px; display: grid; place-items: center; border: 1px solid var(--rose-300); border-radius: 50% 50% 48% 52%; color: var(--rose-700); font-family: Georgia, serif; background: var(--rose-50); transform: rotate(-7deg); }
.brand-copy { display: grid; line-height: 1.1; }
.brand-copy strong { font-family: Georgia, "Songti SC", serif; font-size: 16px; letter-spacing: .02em; }
.brand-copy small { margin-top: 4px; color: var(--muted); font-size: 10px; letter-spacing: .16em; }
.nav-links { display: flex; align-items: center; gap: 4px; }
.nav-links a { padding: 9px 11px; border-radius: 999px; color: var(--muted-strong); font-size: 14px; text-decoration: none; transition: .2s ease; }
.nav-links a:hover, .nav-links a.router-link-exact-active { color: var(--ink); background: var(--rose-50); }
.menu-button { display: none; width: 42px; height: 42px; border: 0; border-radius: 50%; background: var(--rose-50); }
.menu-button span { width: 18px; height: 1px; display: block; margin: 5px auto; background: var(--ink); }
.main-content { flex: 1; padding-top: 68px; }
.site-footer { padding: 56px 24px 34px; text-align: center; color: var(--muted); background: rgba(250, 246, 242, .82); border-top: 1px solid var(--line); }
.footer-flower { width: 42px; height: 42px; display: grid; place-items: center; margin: 0 auto 16px; border: 1px solid var(--rose-200); border-radius: 50%; color: var(--rose-600); }
.site-footer p { margin: 0 0 16px; }
.footer-links { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 18px; font-size: 12px; }
.footer-links a { color: inherit; text-decoration: none; }
.footer-links a:hover { color: var(--rose-700); }

@media (max-width: 860px) {
  .header-inner { width: calc(100% - 28px); height: 62px; }
  .main-content { padding-top: 62px; }
  .menu-button { display: block; }
  .nav-links { position: absolute; top: 62px; left: 14px; right: 14px; padding: 12px; display: grid; grid-template-columns: repeat(2, 1fr); border: 1px solid var(--line); border-radius: 20px; background: var(--paper); box-shadow: var(--shadow-lg); opacity: 0; visibility: hidden; transform: translateY(-8px); transition: .2s ease; }
  .nav-links.open { opacity: 1; visibility: visible; transform: translateY(0); }
  .nav-links a { padding: 12px 14px; }
}
</style>
