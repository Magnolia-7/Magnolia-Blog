<template>
  <div class="post-page">
    <button class="back-link" type="button" @click="router.back()">← 返回记录</button>
    <div v-if="loading" class="state-card">加载中…</div>
    <div v-else-if="error" class="state-card error">{{ error }}</div>
    <article v-else-if="post">
      <header class="post-hero">
        <div class="post-heading">
          <div class="post-kicker"><span>{{ ({ life: "记录贴", study: "技术贴", thought: "说说贴" })[post.category] }}</span><time>{{ formatDate(post.published_at || post.created_at) }}</time></div>
          <h1>{{ post.title }}</h1>
          <p v-if="post.summary">{{ post.summary }}</p>
          <div v-if="post.tags" class="tag-list"><span v-for="tag in splitTags(post.tags)" :key="tag"># {{ tag }}</span></div>
        </div>
        <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" class="hero-cover" />
      </header>
      <div class="article-layout">
        <aside><span class="comic">POST</span><i></i><small>{{ readingMinutes }} min read</small></aside>
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
.post-page{width:min(1060px,calc(100% - 64px));margin:auto;padding:34px 0 64px}.back-link{padding:4px 0;border:0;border-bottom:1px solid currentColor;background:transparent;font-size:12px;margin-bottom:24px}.post-hero{padding:32px;border:1.5px solid var(--ink);background:var(--paper);display:grid;grid-template-columns:minmax(0,1fr);gap:24px}.post-kicker{display:flex;gap:16px;font-size:12px;color:var(--muted)}.post-kicker>span{color:var(--ink)}.post-heading h1{font-size:clamp(26px,4vw,45px);font-weight:500;line-height:1.5;margin:20px 0;overflow-wrap:anywhere}.post-heading>p{font-size:15px;line-height:1.9;color:var(--muted-strong)}.tag-list{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:var(--muted);margin-top:20px}.hero-cover{width:100%;max-height:420px;object-fit:contain}.article-layout{display:grid;grid-template-columns:80px minmax(0,1fr);gap:32px;margin-top:24px}.article-layout aside{align-self:start;display:grid;gap:15px;padding-top:24px;color:var(--muted);font-size:11px}.article-layout aside>.comic{font-size:24px}.article-layout aside i{width:1px;height:60px;background:var(--ink)}.markdown-content{min-width:0;border:1px solid var(--ink);background:var(--paper);padding:32px;font-size:16px;line-height:2;overflow-wrap:anywhere}.markdown-content :deep(h1),.markdown-content :deep(h2),.markdown-content :deep(h3){margin:1.5em 0 .7em;font-weight:500;line-height:1.5}.markdown-content :deep(p){margin:0 0 1.2em}.markdown-content :deep(img){max-width:100%;height:auto;margin:2em auto}.markdown-content :deep(pre){padding:20px;color:#f5f5f1;background:#202020;overflow:auto;white-space:pre}.markdown-content :deep(code){font-family:'SFMono-Regular',Consolas,monospace;font-size:.88em}.markdown-content :deep(:not(pre)>code){background:var(--rose-50);padding:2px 5px}.markdown-content :deep(blockquote){margin:1.5em 0;padding:16px 20px;background:var(--rose-50);border-left:3px solid var(--ink)}.markdown-content :deep(table){border-collapse:collapse;display:block;max-width:100%;overflow:auto}.markdown-content :deep(td),.markdown-content :deep(th){border:1px solid var(--line);padding:8px 12px}.markdown-content :deep(a){text-underline-offset:4px}
@media(max-width:760px){.post-page{width:calc(100% - 44px)}.article-layout{grid-template-columns:1fr;gap:14px}.article-layout aside{display:flex;align-items:center;padding:0}.article-layout aside i{height:1px;width:40px}.post-hero,.markdown-content{padding:24px}}
@media(max-width:480px){.post-page{width:calc(100% - 32px);padding-top:24px}.post-hero,.markdown-content{padding:20px}.markdown-content{font-size:15px}}
</style>
