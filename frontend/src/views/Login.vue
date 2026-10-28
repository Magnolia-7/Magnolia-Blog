<template>
  <div class="login-page">
    <section class="login-card surface">
      <h1 class="comic">LOGIN</h1>
      <form @submit.prevent="handleLogin"><div class="field"><label for="username">用户名</label><input id="username" v-model="form.username" autocomplete="username" required /></div><div class="field"><label for="password">密码</label><input id="password" v-model="form.password" type="password" autocomplete="current-password" required /></div><button class="primary-button" :disabled="loading">{{ loading ? "登录中…" : "进入后台" }}</button></form>
      <p v-if="error" class="error-text">{{ error }}</p><RouterLink to="/">← 返回网站</RouterLink>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue"; import { useRouter } from "vue-router"; import { login } from "../api/auth";
const router = useRouter(); const form = reactive({ username: "", password: "" }); const loading = ref(false); const error = ref("");
async function handleLogin() { loading.value = true; error.value = ""; try { const { data } = await login(form); localStorage.setItem("access_token", data.access_token); router.push("/admin"); } catch { error.value = "用户名或密码不正确。"; } finally { loading.value = false; } }
</script>

<style scoped>
.login-page { min-height: calc(100svh - 68px); padding: 70px 20px; display: grid; place-items: center; }.login-card { width: min(440px, 100%); padding: 42px; text-align: center; }.login-mark { width: 68px; height: 68px; display: grid; place-items: center; margin: 0 auto 22px; border-radius: 50%; color: #fff; background: var(--rose-600); font: 30px Georgia, serif; }.login-card h1 { margin: 0; font: 400 48px Manga, Impact, sans-serif; }.login-card > p:not(.eyebrow):not(.error-text) { color: var(--muted); line-height: 1.7; }.login-card form { display: grid; gap: 17px; margin: 28px 0 18px; text-align: left; }.login-card form button { margin-top: 4px; }.login-card > a { color: var(--muted); font-size: 12px; text-decoration: none; }
</style>
