<template>
  <div class="admin-page">
    <aside class="admin-sidebar">
      <RouterLink to="/" class="admin-brand"><span>M</span><div><strong>Magnolia Nook</strong><small>Content Studio · 2.0</small></div></RouterLink>
      <nav>
        <button v-for="item in tabs" :key="item.value" :class="{ active: activeTab === item.value }" @click="activeTab = item.value"><span>{{ item.icon }}</span>{{ item.label }}</button>
      </nav>
      <div class="sidebar-foot"><RouterLink to="/" target="_blank">查看网站 ↗</RouterLink><button @click="logout">退出登录</button></div>
    </aside>
    <main class="admin-main">
      <header class="admin-topbar"><div><small>MAGNOLIA CONTENT STUDIO</small><h1>{{ currentTitle }}</h1></div><div class="admin-status"><i></i> 已连接</div></header>
      <div class="admin-surface">
        <AdminPosts v-if="activeTab === 'posts'" />
        <AdminMedia v-else-if="activeTab === 'media'" />
        <AdminProfile v-else-if="activeTab === 'profile'" />
        <AdminContent v-else />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import AdminPosts from "../components/admin/AdminPosts.vue";
import AdminMedia from "../components/admin/AdminMedia.vue";
import AdminProfile from "../components/admin/AdminProfile.vue";
import AdminContent from "../components/admin/AdminContent.vue";
const router = useRouter(); const activeTab = ref("posts");
const tabs = [{ value: "posts", label: "文章管理", icon: "✎" }, { value: "media", label: "媒体中心", icon: "▧" }, { value: "profile", label: "主页与关于", icon: "○" }, { value: "content", label: "内容模块", icon: "⌘" }];
const currentTitle = computed(() => tabs.find((item) => item.value === activeTab.value)?.label || "后台管理");
function logout() { localStorage.removeItem("access_token"); router.push("/login"); }
</script>

<style scoped>
.admin-page { min-height: calc(100vh - 68px); display: grid; grid-template-columns: 248px 1fr; background: #f6f3ef; }.admin-sidebar { position: sticky; top: 68px; height: calc(100vh - 68px); padding: 26px 18px; display: flex; flex-direction: column; border-right: 1px solid var(--line); background: #2e2928; }.admin-brand { display: flex; align-items: center; gap: 10px; padding: 0 8px 26px; color: #fff; text-decoration: none; }.admin-brand > span { width: 37px; height: 37px; display: grid; place-items: center; border: 1px solid rgba(255,255,255,.3); border-radius: 50%; font-family: Georgia, serif; }.admin-brand div { display: grid; gap: 4px; }.admin-brand strong { font: 15px Georgia, serif; }.admin-brand small { color: rgba(255,255,255,.48); font-size: 9px; letter-spacing: .08em; }.admin-sidebar nav { display: grid; gap: 5px; }.admin-sidebar nav button { padding: 12px 14px; display: flex; gap: 11px; align-items: center; border: 0; border-radius: 10px; color: rgba(255,255,255,.65); text-align: left; background: transparent; }.admin-sidebar nav button:hover, .admin-sidebar nav button.active { color: #fff; background: rgba(255,255,255,.09); }.admin-sidebar nav span { width: 20px; color: #dba9b5; }.sidebar-foot { margin-top: auto; display: grid; gap: 6px; padding-top: 18px; border-top: 1px solid rgba(255,255,255,.1); }.sidebar-foot a, .sidebar-foot button { padding: 9px 12px; border: 0; color: rgba(255,255,255,.55); font-size: 12px; text-align: left; text-decoration: none; background: transparent; }.admin-main { min-width: 0; padding: 32px clamp(20px, 4vw, 54px) 70px; }.admin-topbar { max-width: 1160px; margin: 0 auto 24px; display: flex; justify-content: space-between; align-items: end; }.admin-topbar small { color: var(--rose-600); font-size: 9px; letter-spacing: .17em; }.admin-topbar h1 { margin: 5px 0 0; font: 500 37px Georgia, "Songti SC", serif; }.admin-status { display: flex; align-items: center; gap: 7px; color: var(--muted); font-size: 11px; }.admin-status i { width: 7px; height: 7px; border-radius: 50%; background: #6e9c78; box-shadow: 0 0 0 4px rgba(110,156,120,.12); }.admin-surface { max-width: 1160px; min-height: 500px; margin: 0 auto; padding: clamp(20px, 3vw, 34px); border: 1px solid var(--line); border-radius: 22px; background: var(--paper); box-shadow: var(--shadow-sm); }
@media (max-width: 780px) { .admin-page { grid-template-columns: 1fr; }.admin-sidebar { position: static; width: 100%; height: auto; padding: 12px; }.admin-brand { padding: 4px 4px 12px; }.admin-sidebar nav { grid-template-columns: repeat(4, 1fr); }.admin-sidebar nav button { justify-content: center; padding: 10px 4px; font-size: 11px; }.admin-sidebar nav span { display: none; }.sidebar-foot { display: none; }.admin-main { padding: 22px 14px 60px; }.admin-topbar { align-items: center; }.admin-topbar h1 { font-size: 28px; } }
</style>
