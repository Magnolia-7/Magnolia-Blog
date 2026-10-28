<template>
  <div class="page-shell home-page">
    <section class="home-hero"><img :src="heroImage" alt="草帽一伙漫画合照" fetchpriority="high" /><h1 class="comic">{{ nickname }}</h1></section>
    <section aria-label="站点统计"><div class="section-row stats-title"><h2 class="comic">SITE STATS</h2><button v-if="statsError" class="text-button error-text" type="button" @click="loadStats">统计加载失败，重试</button></div><div class="site-stats"><div><strong class="comic">{{ number(stats?.visitors) }}</strong><span>访客数 · UV</span></div><div><strong class="comic">{{ number(stats?.page_views) }}</strong><span>访问量 · PV</span></div><div><strong class="comic">{{ number(stats?.articles) }}</strong><span>文章</span></div><div><strong class="comic">{{ number(stats?.running_days) }}<small>DAYS</small></strong><span>站点运行</span></div></div></section>
    <section class="latest-section"><header class="section-row ruled-heading"><h2 class="comic">LATEST</h2><RouterLink class="text-link" to="/records">全部记录 ↗</RouterLink></header><div v-if="loading" class="state-card" role="status">加载中…</div><div v-else-if="postsError" class="state-card error" role="alert">文章加载失败。<button class="text-button" type="button" @click="loadPosts">重试</button></div><div v-else-if="!posts.length" class="state-card">暂无文章</div><div v-else class="latest-grid"><PostCard v-for="post in posts" :key="post.id" :post="post" /></div></section>
  </div>
</template>
<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { getSiteStats } from '../api/activity';
import { getPosts } from '../api/posts';
import { getAbout } from '../api/about';
import { useSite } from '../composables/site';
import PostCard from '../components/PostCard.vue';
const { heroImage } = useSite();
const nickname = ref('MAGNOLIA'), stats = ref(null), statsError = ref(false), posts = ref([]), loading = ref(true), postsError = ref(false);
const number = (value) => value == null ? '—' : value.toLocaleString('zh-CN');
async function loadStats() { try { stats.value = (await getSiteStats()).data; statsError.value = false; } catch { statsError.value = true; } }
async function loadPosts() { loading.value = true; postsError.value = false; try { posts.value = (await getPosts({ page_size: 4 })).data.items; } catch { postsError.value = true; } finally { loading.value = false; } }
onMounted(() => { loadStats(); loadPosts(); getAbout().then(({ data }) => { if (data?.nickname) nickname.value = data.nickname; }).catch(() => {}); window.addEventListener('site-stats-updated', loadStats); });
onUnmounted(() => window.removeEventListener('site-stats-updated', loadStats));
</script>
