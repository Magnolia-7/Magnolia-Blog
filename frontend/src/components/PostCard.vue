<template>
  <RouterLink :to="`/posts/${post.id}`" class="post-card surface">
    <div class="post-meta"><span class="post-tag">{{ categoryLabel(post.category) }}</span><time>{{ formatDate(post.published_at || post.created_at) }}</time></div>
    <h2>{{ post.title }}</h2>
    <p v-if="post.summary">{{ post.summary }}</p>
    <div v-if="post.is_pinned || post.tags" class="post-tags"><span v-if="post.is_pinned">置顶</span><span v-for="tag in tags(post.tags)" :key="tag"># {{ tag }}</span></div>
  </RouterLink>
</template>
<script setup>
import { categoryLabel, formatDate, tags } from '../utils/format';
defineProps({ post: { type: Object, required: true } });
</script>
