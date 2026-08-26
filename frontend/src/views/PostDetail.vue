<template>
  <div class="post-page">
    <button class="back-link" type="button" @click="router.back()">← 返回记录</button>
    <div v-if="loading" class="state-card">正在翻开这一页…</div>
    <div v-else-if="error" class="state-card error">{{ error }}</div>
    <article v-else-if="post">
      <header class="post-hero">
        <div class="post-heading">
          <div class="post-kicker"><span>{{ post.category === "life" ? "生活记录" : "学习笔记" }}</span><time>{{ formatDate(post.published_at || post.created_at) }}</time></div>
          <h1>{{ post.title }}</h1>
          <p v-if="post.summary">{{ post.summary }}</p>
          <div v-if="post.tags" class="tag-list"><span v-for="tag in splitTags(post.tags)" :key="tag"># {{ tag }}</span></div>
        </div>
        <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" class="hero-cover" />
      </header>
      <div class="article-layout">
        <aside><span>MAGNOLIA<br />NOOK</span><i></i><small>{{ readingMinutes }} min read</small></aside>
        <div class="markdown-content" v-html="renderedContent"></div>
      </div>
    </article>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"; import { useRoute, useRouter } from "vue-router"; import { getPostDetail } from "../api/posts"; import { renderMarkdown } from "../utils/markdown";
const route = useRoute(); const router = useRouter(); const post = ref(null); const loading = ref(true); const error = ref("");
const renderedContent = computed(() => renderMarkdown(post.value?.content || "")); const readingMinutes = computed(() => Math.max(1, Math.ceil((post.value?.content?.length || 0) / 500)));
function formatDate(value) { return new Date(value).toLocaleDateString("zh-CN", { year: "numeric", month: "long", day: "numeric" }); }
function splitTags(value) { return value.split(/[,，]/).map((tag) => tag.trim()).filter(Boolean); }
onMounted(async () => { try { post.value = (await getPostDetail(route.params.id)).data; } catch { error.value = "文章不存在、尚未发布，或者暂时无法访问。"; } finally { loading.value = false; } });
</script>

<style scoped>
.post-page { width: min(1060px, calc(100% - 40px)); margin: 0 auto; padding: 52px 0 100px; }.back-link { margin-bottom: 34px; padding: 0; border: 0; color: var(--muted); background: transparent; }.back-link:hover { color: var(--rose-700); }.post-hero { padding-bottom: 50px; display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(280px, .9fr); gap: 48px; align-items: center; border-bottom: 1px solid var(--line); }.post-hero:not(:has(.hero-cover)) { grid-template-columns: 1fr; }.post-kicker { display: flex; gap: 16px; color: var(--muted); font-size: 11px; letter-spacing: .1em; }.post-kicker span { color: var(--rose-600); font-weight: 750; }.post-heading h1 { margin: 18px 0 22px; font: 500 clamp(42px, 6vw, 72px)/1.18 Georgia, "Songti SC", serif; letter-spacing: -.04em; }.post-heading > p { max-width: 680px; color: var(--muted-strong); font-size: 17px; line-height: 1.9; }.tag-list { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; color: var(--rose-600); font-size: 11px; }.hero-cover { width: 100%; aspect-ratio: 1.15; object-fit: cover; border-radius: 180px 180px 22px 22px; box-shadow: var(--shadow-lg); }.article-layout { display: grid; grid-template-columns: 110px minmax(0, 760px); gap: 50px; justify-content: center; padding-top: 58px; }.article-layout aside { position: sticky; top: 100px; height: max-content; display: grid; gap: 15px; color: var(--muted); font-size: 9px; letter-spacing: .16em; }.article-layout aside i { width: 1px; height: 70px; background: var(--rose-300); }.markdown-content { min-width: 0; color: #453e3c; font-family: "Songti SC", Georgia, serif; font-size: 18px; line-height: 2.08; }.markdown-content :deep(h1), .markdown-content :deep(h2), .markdown-content :deep(h3) { margin: 1.55em 0 .65em; color: var(--ink); font-family: Georgia, "Songti SC", serif; font-weight: 550; line-height: 1.4; }.markdown-content :deep(p) { margin: 0 0 1.2em; }.markdown-content :deep(img) { display: block; max-width: 100%; margin: 2em auto; border-radius: 18px; box-shadow: var(--shadow-sm); }.markdown-content :deep(blockquote) { margin: 1.8em 0; padding: 18px 22px; border-left: 2px solid var(--rose-500); color: var(--muted-strong); background: var(--rose-50); }.markdown-content :deep(pre) { padding: 20px; border-radius: 14px; color: #f7f2ed; background: #2d2928; overflow: auto; }.markdown-content :deep(code) { font-family: "SFMono-Regular", Consolas, monospace; font-size: .88em; }.markdown-content :deep(:not(pre) > code) { padding: 2px 6px; border-radius: 5px; color: var(--rose-700); background: var(--rose-50); }.markdown-content :deep(a) { color: var(--rose-700); text-underline-offset: 4px; }
@media (max-width: 760px) { .post-page { width: calc(100% - 28px); }.post-hero { grid-template-columns: 1fr; }.hero-cover { max-height: 450px; }.article-layout { grid-template-columns: 1fr; }.article-layout aside { position: static; display: flex; align-items: center; }.article-layout aside i { width: 50px; height: 1px; }.markdown-content { font-size: 17px; } }
</style>
