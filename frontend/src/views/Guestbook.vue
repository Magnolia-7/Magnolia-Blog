<template>
  <div class="page-shell guestbook-page">
    <header class="page-heading"><p class="eyebrow">Leave a note</p><h1>来都来了，留句话吧</h1><p>可以是一句问候、一段想法，也可以分享最近让你开心的小事。</p></header>
    <section class="guest-layout">
      <form class="message-form surface" @submit.prevent="submitMessage">
        <h2>写下留言</h2>
        <div class="field"><label for="nickname">怎么称呼你</label><input id="nickname" v-model="form.nickname" maxlength="80" required placeholder="你的昵称" /></div>
        <div class="field"><label for="website">个人主页（可选）</label><input id="website" v-model="form.website" type="url" placeholder="https://" /></div>
        <div class="honeypot" aria-hidden="true"><input v-model="form.company" tabindex="-1" autocomplete="off" /></div>
        <div class="field"><label for="message">想说的话</label><textarea id="message" v-model="form.content" rows="7" minlength="2" maxlength="1000" required placeholder="写点什么吧…"></textarea><small>{{ form.content.length }}/1000</small></div>
        <button class="primary-button" :disabled="submitting">{{ submitting ? "正在送出…" : "送出留言" }}</button>
        <p v-if="notice" :class="success ? 'success-text' : 'error-text'">{{ notice }}</p>
      </form>
      <div class="message-wall">
        <div class="wall-title"><span>MESSAGE WALL</span><strong>{{ messages.length.toString().padStart(2, "0") }}</strong></div>
        <div v-if="loading" class="state-card">正在读取留言…</div>
        <div v-else-if="!messages.length" class="state-card">成为第一个留下足迹的人吧。</div>
        <article v-for="message in messages" :key="message.id" class="message-card surface">
          <div class="message-author"><span>{{ message.nickname.slice(0, 1) }}</span><div><a v-if="message.website" :href="message.website" target="_blank">{{ message.nickname }}</a><strong v-else>{{ message.nickname }}</strong><time>{{ formatDate(message.created_at) }}</time></div></div>
          <p>{{ message.content }}</p>
          <div v-if="message.admin_reply" class="reply"><small>站长回复</small><p>{{ message.admin_reply }}</p></div>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { createGuestbookMessage, getGuestbook } from "../api/content";
const form = reactive({ nickname: "", website: "", content: "", company: "" }); const messages = ref([]); const loading = ref(true); const submitting = ref(false); const notice = ref(""); const success = ref(false);
async function loadMessages() { try { messages.value = (await getGuestbook()).data; } finally { loading.value = false; } }
async function submitMessage() { submitting.value = true; notice.value = ""; try { const { data } = await createGuestbookMessage(form); notice.value = data.detail; success.value = true; Object.assign(form, { nickname: "", website: "", content: "", company: "" }); } catch (error) { notice.value = error.response?.data?.detail || "留言提交失败，请稍后再试。"; success.value = false; } finally { submitting.value = false; } }
function formatDate(value) { return new Date(value).toLocaleDateString("zh-CN", { month: "short", day: "numeric", year: "numeric" }); }
onMounted(loadMessages);
</script>

<style scoped>
.guest-layout { display: grid; grid-template-columns: minmax(300px, .72fr) minmax(0, 1.28fr); gap: 54px; align-items: start; }.message-form { position: sticky; top: 96px; padding: 30px; display: grid; gap: 18px; }.message-form h2 { margin: 0 0 4px; font: 500 28px Georgia, "Songti SC", serif; }.field small { justify-self: end; color: var(--muted); font-size: 11px; }.honeypot { position: absolute; left: -9999px; }.wall-title { margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; color: var(--muted); font-size: 11px; letter-spacing: .16em; }.wall-title strong { color: var(--rose-300); font: 60px Georgia, serif; }.message-wall { display: grid; gap: 15px; }.message-card { padding: 24px; }.message-author { display: flex; gap: 12px; align-items: center; }.message-author > span { width: 40px; height: 40px; display: grid; place-items: center; border-radius: 50%; color: var(--rose-700); background: var(--rose-50); font-family: Georgia, serif; }.message-author div { display: grid; gap: 3px; }.message-author a, .message-author strong { font-size: 14px; text-decoration: none; }.message-author time { color: var(--muted); font-size: 11px; }.message-card > p { margin: 20px 0 0; color: var(--muted-strong); line-height: 1.85; white-space: pre-line; }.reply { margin-top: 18px; padding: 16px; border-radius: 13px; background: var(--rose-50); }.reply small { color: var(--rose-600); font-weight: 750; }.reply p { margin: 6px 0 0; line-height: 1.75; }
@media (max-width: 800px) { .guest-layout { grid-template-columns: 1fr; }.message-form { position: static; } }
</style>
