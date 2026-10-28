<template>
  <div class="page-shell"><header class="page-heading"><h1>FRIENDS</h1></header><div v-if="loading" class="state-card" role="status">加载中…</div><div v-else-if="error" class="state-card error" role="alert">友链加载失败。 <button class="text-button" type="button" @click="load">重试</button></div><div v-else-if="!friends.length" class="state-card">暂无友链</div><div v-else class="friends-grid"><a v-for="friend in friends" :key="friend.id" class="friend-card surface" :href="friend.url" target="_blank" rel="noopener noreferrer"><img v-if="friend.avatar_url" :src="friend.avatar_url" :alt="friend.name" loading="lazy" /><span v-else class="friend-letter comic" aria-hidden="true">{{ friend.name.slice(0, 1) }}</span><div><h2>{{ friend.name }} ↗</h2><p v-if="friend.description">{{ friend.description }}</p></div></a></div></div>
</template>
<script setup>
import { onMounted, ref } from 'vue';
import { getFriendLinks } from '../api/content';
const friends = ref([]), loading = ref(true), error = ref(false);
async function load() { loading.value = true; error.value = false; try { friends.value = (await getFriendLinks()).data; } catch { error.value = true; } finally { loading.value = false; } }
onMounted(load);
</script>
