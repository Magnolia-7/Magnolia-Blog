<template>
  <div class="post-detail-page">
    <!-- 返回入口 -->
    <button class="back-btn" @click="goBack">
      返回
    </button>

    <!-- 状态提示 -->
    <div v-if="loading" class="state-card">加载中...</div>
    <div v-else-if="error" class="state-card error">{{ error }}</div>

    <!-- 文章详情 -->
    <article v-else-if="post" class="post-article">
      <header class="post-header">
        <p class="eyebrow">{{ formatCategory(post.category) }}</p>

        <h1>{{ post.title }}</h1>

        <p class="meta">
          发布时间：{{ formatDate(post.created_at) }}
        </p>

        <p v-if="post.summary" class="summary">
          {{ post.summary }}
        </p>
      </header>

      <div class="markdown-content" v-html="renderedContent"></div>
    </article>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getPostDetail } from "../api/posts";
import { renderMarkdown } from "../utils/markdown";

const route = useRoute();
const router = useRouter();

const post = ref(null);
const loading = ref(false);
const error = ref("");
const renderedContent = computed(() => renderMarkdown(post.value?.content || ""));

async function loadPostDetail() {
  loading.value = true;
  error.value = "";

  try {
    const postId = route.params.id;
    const response = await getPostDetail(postId);
    post.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = "文章详情加载失败，可能文章不存在或未发布。";
  } finally {
    loading.value = false;
  }
}

function goBack() {
  router.back();
}

function formatCategory(category) {
  if (category === "life") return "生活记录";
  if (category === "study") return "学习笔记";
  return category || "未分类";
}

function formatDate(dateString) {
  if (!dateString) return "";
  return new Date(dateString).toLocaleString();
}

onMounted(() => {
  loadPostDetail();
});
</script>

<style scoped>
.post-detail-page {
  max-width: 880px;
  margin: 0 auto;
  padding: 56px 24px 76px;
}

.back-btn {
  margin-bottom: 24px;
  padding: 9px 16px;
  border: 1px solid rgba(216, 154, 170, 0.28);
  border-radius: 999px;
  color: #8f5f6b;
  background: rgba(255, 255, 255, 0.62);
  transition:
    color 0.2s ease,
    background 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease;
}

.back-btn:hover {
  color: #ffffff;
  border-color: #b87b8b;
  background: #b87b8b;
  transform: translateY(-1px);
}

.state-card {
  padding: 18px 20px;
  border: 1px solid rgba(90, 50, 64, 0.08);
  border-radius: 18px;
  color: #6f6065;
  background: rgba(255, 255, 255, 0.68);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.error {
  color: #c0392b;
}

.post-article {
  padding: 44px 48px 52px;
  border: 1px solid rgba(90, 50, 64, 0.08);
  border-radius: 30px;
  background: rgba(255, 255, 255, 0.74);
  box-shadow: 0 24px 72px rgba(90, 50, 64, 0.06);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.post-header {
  padding-bottom: 30px;
  border-bottom: 1px solid rgba(90, 50, 64, 0.08);
}

.eyebrow {
  margin: 0 0 14px;
  color: #b87b8b;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.post-header h1 {
  margin: 0;
  color: #151515;
  font-size: 42px;
  line-height: 1.2;
  letter-spacing: -1.2px;
}

.meta {
  margin: 18px 0 0;
  color: #8b7c82;
  font-size: 14px;
}

.summary {
  margin: 26px 0 0;
  padding: 18px 20px;
  border-left: 3px solid #b87b8b;
  border-radius: 14px;
  color: #5d5558;
  line-height: 1.9;
  background: rgba(255, 241, 245, 0.62);
}

.markdown-content {
  margin-top: 34px;
  color: #3f383b;
  font-size: 17px;
  line-height: 2.05;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  margin: 1.4em 0 0.6em;
  color: #151515;
  line-height: 1.35;
  letter-spacing: -0.4px;
}

.markdown-content :deep(h1:first-child),
.markdown-content :deep(h2:first-child),
.markdown-content :deep(h3:first-child),
.markdown-content :deep(p:first-child) {
  margin-top: 0;
}

.markdown-content :deep(p) {
  margin: 0 0 1.1em;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin: 0 0 1.2em;
  padding-left: 1.5em;
}

.markdown-content :deep(li) {
  margin: 0.35em 0;
}

.markdown-content :deep(blockquote) {
  margin: 1.4em 0;
  padding: 14px 18px;
  border-left: 3px solid #b87b8b;
  border-radius: 12px;
  color: #5d5558;
  background: rgba(255, 241, 245, 0.62);
}

.markdown-content :deep(pre) {
  overflow: auto;
  margin: 1.4em 0;
  padding: 18px;
  border-radius: 14px;
  color: #f8f8f2;
  background: #2f2a2c;
}

.markdown-content :deep(code) {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 0.92em;
}

.markdown-content :deep(:not(pre) > code) {
  padding: 2px 6px;
  border-radius: 6px;
  color: #9f6473;
  background: #fff1f5;
}

.markdown-content :deep(a) {
  color: #9f6473;
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
}

.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1.4em auto;
  border-radius: 16px;
}

.markdown-content :deep(hr) {
  height: 1px;
  margin: 2em 0;
  border: 0;
  background: rgba(90, 50, 64, 0.12);
}

@media (max-width: 720px) {
  .post-detail-page {
    padding: 42px 18px 58px;
  }

  .post-article {
    padding: 30px 24px 36px;
    border-radius: 24px;
  }

  .post-header h1 {
    font-size: 32px;
  }

  .markdown-content {
    font-size: 16px;
    line-height: 1.95;
  }
}
</style>
