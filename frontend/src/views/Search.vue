<template>
  <div class="page-shell search-page"><header class="page-heading"><h1>SEARCH</h1></header><form class="search-form surface" @submit.prevent="search"><div class="search-input-row"><label class="sr-only" for="search-keyword">搜索文章</label><input id="search-keyword" v-model.trim="filters.q" type="search" placeholder="搜索文章" /><button class="primary-button" :disabled="loading">搜索</button></div><div class="search-filters"><div class="field"><label for="search-category">类型</label><select id="search-category" v-model="filters.category"><option value="">全部</option><option value="life">记录贴</option><option value="study">技术贴</option><option value="thought">说说贴</option></select></div><div class="field"><label for="search-start">开始日期</label><input id="search-start" v-model="filters.start_date" type="date" /></div><div class="field"><label for="search-end">结束日期</label><input id="search-end" v-model="filters.end_date" type="date" :min="filters.start_date || undefined" /></div></div></form><div v-if="loading" class="state-card" role="status">搜索中…</div><div v-else-if="error" class="state-card error" role="alert">{{ error }}</div><template v-else><p class="result-count" aria-live="polite">{{ posts.length }} 篇</p><div v-if="!posts.length" class="state-card">暂无结果</div><div v-else class="search-results"><PostCard v-for="post in posts" :key="post.id" :post="post" /></div></template></div>
</template>
<script setup>
import { onMounted, reactive, ref } from 'vue';
import { searchPosts } from '../api/posts';
import PostCard from '../components/PostCard.vue';
const filters = reactive({ q: '', category: '', start_date: '', end_date: '' }), posts = ref([]), loading = ref(false), error = ref('');
let loadId = 0;
async function search() { if (filters.start_date && filters.end_date && filters.start_date > filters.end_date) { error.value = '开始日期不能晚于结束日期。'; return; } const id = ++loadId; loading.value = true; error.value = ''; try { const params = Object.fromEntries(Object.entries(filters).filter(([, v]) => v)); const { data } = await searchPosts(params); if (id === loadId) posts.value = data; } catch { if (id === loadId) error.value = '搜索失败，请重试。'; } finally { if (id === loadId) loading.value = false; } }
onMounted(search);
</script>
