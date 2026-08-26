<template>
  <div class="page-shell changelog-page">
    <header class="page-heading"><p class="eyebrow">Release notes</p><h1>网站更新日志</h1><p>这里记录 Magnolia Nook 的每一次生长，也保留那些看似细小但重要的改变。</p></header>
    <div v-if="loading" class="state-card">正在读取版本记录…</div>
    <div v-else-if="!entries.length" class="state-card">第一份更新日志正在准备中。</div>
    <section v-else class="release-list">
      <article v-for="(entry, index) in entries" :key="entry.id" class="release-entry">
        <div class="release-axis"><span></span><i></i></div>
        <div class="release-card surface">
          <div class="release-head"><div><small>{{ typeLabel(entry.change_type) }}</small><h2>v{{ entry.version }} · {{ entry.title }}</h2></div><time>{{ formatDate(entry.published_at || entry.created_at) }}</time></div>
          <div class="release-content" v-html="renderMarkdown(entry.content)"></div>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getChangelog } from "../api/content";
import { renderMarkdown } from "../utils/markdown";
const entries = ref([]); const loading = ref(true);
function typeLabel(value) { return ({ feature: "新增", improvement: "优化", fix: "修复" })[value] || "更新"; }
function formatDate(value) { return new Date(value).toLocaleDateString("zh-CN", { year: "numeric", month: "long", day: "numeric" }); }
onMounted(async () => { try { entries.value = (await getChangelog()).data; } finally { loading.value = false; } });
</script>

<style scoped>
.release-list { max-width: 920px; margin: 0 auto; }.release-entry { display: grid; grid-template-columns: 54px 1fr; gap: 18px; }.release-axis { position: relative; display: flex; justify-content: center; }.release-axis span { z-index: 1; width: 16px; height: 16px; margin-top: 30px; border: 4px solid var(--paper); border-radius: 50%; background: var(--rose-500); box-shadow: 0 0 0 1px var(--rose-300); }.release-axis i { position: absolute; top: 45px; bottom: -2px; width: 1px; background: var(--rose-200); }.release-entry:last-child .release-axis i { display: none; }.release-card { margin-bottom: 26px; padding: 28px 32px; }.release-head { display: flex; justify-content: space-between; gap: 24px; padding-bottom: 22px; border-bottom: 1px solid var(--line); }.release-head small { color: var(--rose-600); font-weight: 750; letter-spacing: .12em; }.release-head h2 { margin: 7px 0 0; font: 500 27px Georgia, "Songti SC", serif; }.release-head time { color: var(--muted); font-size: 12px; white-space: nowrap; }.release-content { margin-top: 22px; color: var(--muted-strong); line-height: 1.85; }.release-content :deep(p:first-child) { margin-top: 0; }.release-content :deep(p:last-child) { margin-bottom: 0; }
@media (max-width: 600px) { .release-entry { grid-template-columns: 28px 1fr; gap: 8px; }.release-card { padding: 22px; }.release-head { display: block; }.release-head time { display: block; margin-top: 10px; } }
</style>
