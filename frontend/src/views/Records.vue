<template>
  <div class="page-shell records-page">
    <header class="page-heading"><h1>POSTS</h1></header>
    <div class="pill-tabs" aria-label="记录区域"><button v-for="tab in tabs" :key="tab.value" type="button" :class="{ active: activeView === tab.value }" :aria-pressed="activeView === tab.value" @click="switchView(tab.value)">{{ tab.label }}</button></div>
    <section v-if="activeView === 'calendar'" class="calendar-section" aria-label="投入日历"><TimeCalendar standalone /></section>
    <section v-else aria-label="文章列表"><div v-if="loading" class="state-card" role="status">加载中…</div><div v-else-if="error" class="state-card error" role="alert">{{ error }} <button type="button" class="text-button" @click="load">重试</button></div><div v-else-if="!posts.length" class="state-card">暂无文章</div><div v-else class="records-post-grid"><PostCard v-for="post in posts" :key="post.id" :post="post" /></div><nav v-if="totalPages > 1" class="pagination" aria-label="文章分页"><button class="secondary-button" type="button" :disabled="page === 1 || loading" @click="changePage(page - 1)">上一页</button><span>{{ page }} / {{ totalPages }}</span><button class="secondary-button" type="button" :disabled="page >= totalPages || loading" @click="changePage(page + 1)">下一页</button></nav></section>
  </div>
</template>
<script setup>
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getPosts } from '../api/posts';
import PostCard from '../components/PostCard.vue';
import TimeCalendar from '../components/TimeCalendar.vue';
const route = useRoute(), router = useRouter();
const tabs = [{ value: 'all', label: '全部' }, { value: 'life', label: '记录贴' }, { value: 'study', label: '技术贴' }, { value: 'thought', label: '说说贴' }, { value: 'calendar', label: '日历' }];
const posts = ref([]), activeView = ref('all'), page = ref(1), totalPages = ref(0), loading = ref(true), error = ref('');
let loadId = 0;
async function load() { const id = ++loadId; loading.value = true; error.value = ''; try { const { data } = await getPosts({ category: activeView.value === 'all' ? undefined : activeView.value, page: page.value, page_size: 9 }); if (id === loadId) { posts.value = data.items; totalPages.value = data.total_pages; } } catch { if (id === loadId) error.value = '文章加载失败。'; } finally { if (id === loadId) loading.value = false; } }
function switchView(value) { router.replace({ query: { ...route.query, view: value } }); }
function changePage(value) { page.value = value; load(); }
watch(() => route.query.view, (view) => { activeView.value = tabs.some((tab) => tab.value === view) ? view : 'all'; page.value = 1; if (activeView.value !== 'calendar') load(); else ++loadId; }, { immediate: true });
</script>
