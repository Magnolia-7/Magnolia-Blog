<template>
  <div class="page-shell search-page">
    <header class="page-heading"><p class="eyebrow">Search the archive</p><h1>在时间里寻找</h1><p>按名字定位一篇记录，或选择一段时间，看看那时留下了什么。</p></header>
    <form class="search-panel surface" @submit.prevent="handleSearch">
      <div class="keyword-row"><span>⌕</span><input v-model="filters.q" aria-label="搜索关键词" placeholder="输入标题、正文或标签…" /><button class="primary-button">搜索</button></div>
      <div class="filter-row">
        <div class="field"><label>内容类型</label><select v-model="filters.category"><option value="">全部内容</option><option value="life">生活记录</option><option value="study">学习笔记</option></select></div>
        <div class="field"><label>开始日期</label><input v-model="filters.start_date" type="date" /></div>
        <div class="date-arrow">→</div>
        <div class="field"><label>结束日期</label><input v-model="filters.end_date" type="date" /></div>
        <button type="button" class="clear-button" @click="clearFilters">清空</button>
      </div>
    </form>

    <div class="result-head"><p>{{ searched ? `找到 ${results.length} 条记录` : "可以只选择日期，不必填写关键词" }}</p><span v-if="searched">{{ summary }}</span></div>
    <div v-if="loading" class="state-card">正在翻找档案…</div>
    <div v-else-if="error" class="state-card error">{{ error }}</div>
    <div v-else-if="searched && !results.length" class="state-card">没有找到匹配的内容，换一个词或时间试试。</div>
    <section v-else-if="results.length" class="timeline-results">
      <article v-for="post in results" :key="post.id" class="result-card">
        <time><strong>{{ day(post.created_at) }}</strong><span>{{ monthYear(post.created_at) }}</span></time>
        <div class="timeline-dot"></div>
        <RouterLink class="result-copy surface" :to="`/posts/${post.id}`">
          <div><small>{{ post.category === "life" ? "生活记录" : "学习笔记" }}</small><span v-if="post.tags">{{ post.tags }}</span></div>
          <h2>{{ post.title }}</h2><p>{{ post.summary || "没有摘要" }}</p>
        </RouterLink>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { searchPosts } from "../api/posts";
const filters = reactive({ q: "", category: "", start_date: "", end_date: "" }); const results = ref([]); const searched = ref(false); const loading = ref(false); const error = ref("");
const summary = computed(() => [filters.q && `关键词「${filters.q}」`, filters.category && (filters.category === "life" ? "生活记录" : "学习笔记"), (filters.start_date || filters.end_date) && "指定时间段"].filter(Boolean).join(" · "));
async function handleSearch() { if (![filters.q, filters.category, filters.start_date, filters.end_date].some(Boolean)) { error.value = "请输入关键词或至少选择一个筛选条件。"; return; } loading.value = true; error.value = ""; searched.value = true; try { const params = Object.fromEntries(Object.entries(filters).filter(([, value]) => value)); results.value = (await searchPosts(params)).data; } catch { error.value = "搜索失败，请稍后重试。"; } finally { loading.value = false; } }
function clearFilters() { Object.assign(filters, { q: "", category: "", start_date: "", end_date: "" }); results.value = []; searched.value = false; error.value = ""; }
function day(value) { return new Date(value).getDate().toString().padStart(2, "0"); }
function monthYear(value) { return new Date(value).toLocaleDateString("zh-CN", { year: "numeric", month: "short" }); }
</script>

<style scoped>
.search-panel { padding: 20px; }.keyword-row { display: grid; grid-template-columns: 34px 1fr auto; align-items: center; gap: 8px; padding-bottom: 18px; border-bottom: 1px solid var(--line); }.keyword-row > span { color: var(--rose-600); font-size: 28px; }.keyword-row input { min-width: 0; border: 0; outline: 0; color: var(--ink); background: transparent; font: 500 clamp(18px, 2vw, 23px) Georgia, "Songti SC", serif; }.filter-row { display: grid; grid-template-columns: 1fr 1fr auto 1fr auto; align-items: end; gap: 14px; padding-top: 18px; }.date-arrow { padding-bottom: 13px; color: var(--rose-400); }.clear-button { min-height: 42px; border: 0; color: var(--muted); background: transparent; }.result-head { min-height: 76px; margin-top: 24px; display: flex; justify-content: space-between; align-items: center; color: var(--muted); font-size: 13px; }.result-head span { color: var(--rose-600); }.timeline-results { max-width: 900px; margin: 0 auto; }.result-card { display: grid; grid-template-columns: 72px 24px 1fr; gap: 14px; min-height: 175px; }.result-card > time { padding-top: 24px; text-align: right; }.result-card time strong { display: block; color: var(--rose-600); font: 34px Georgia, serif; }.result-card time span { color: var(--muted); font-size: 10px; }.timeline-dot { position: relative; }.timeline-dot::before { content: ""; position: absolute; top: 34px; left: 50%; width: 7px; height: 7px; border-radius: 50%; background: var(--rose-500); transform: translateX(-50%); }.timeline-dot::after { content: ""; position: absolute; top: 41px; bottom: 0; left: 50%; width: 1px; background: var(--rose-200); }.result-card:last-child .timeline-dot::after { display: none; }.result-copy { margin-bottom: 18px; padding: 22px 25px; text-decoration: none; transition: .2s ease; }.result-copy:hover { transform: translateX(4px); }.result-copy > div { display: flex; gap: 14px; color: var(--muted); font-size: 11px; }.result-copy small { color: var(--rose-600); font-weight: 750; }.result-copy h2 { margin: 10px 0 7px; font: 500 24px Georgia, "Songti SC", serif; }.result-copy p { margin: 0; color: var(--muted-strong); }
@media (max-width: 700px) { .filter-row { grid-template-columns: 1fr 1fr; }.date-arrow { display: none; }.result-card { grid-template-columns: 52px 14px 1fr; gap: 7px; }.result-card time strong { font-size: 26px; }.result-copy { padding: 19px; } }
</style>
