<template>
  <div class="records-page">
    <!-- 页面标题区域 -->
    <header class="records-header">
      <p class="eyebrow">Journal</p>
      <h1>记录</h1>
    </header>

    <!-- 分类切换 -->
    <div class="tabs">
      <button
        :class="{ active: activeCategory === '' }"
        @click="loadPosts('')"
      >
        全部
      </button>
      <button
        :class="{ active: activeCategory === 'life' }"
        @click="loadPosts('life')"
      >
        生活记录
      </button>
      <button
        :class="{ active: activeCategory === 'study' }"
        @click="loadPosts('study')"
      >
        学习笔记
      </button>
    </div>

    <!-- 状态提示 -->
    <div v-if="loading" class="state-card">加载中...</div>
    <div v-else-if="error" class="state-card error">{{ error }}</div>
    <div v-else-if="posts.length === 0" class="state-card">
      暂无文章
    </div>

    <!-- 三列文章卡片 -->
    <div v-else class="post-list">
      <article v-for="post in posts" :key="post.id" class="post-card">
        <RouterLink class="cover-link" :to="`/posts/${post.id}`">
          <img
            v-if="post.cover_image"
            class="cover-image"
            :src="post.cover_image"
            :alt="post.title"
          />
          <div v-else class="cover-placeholder">
            Magnolia Nook
          </div>
        </RouterLink>

        <div class="post-content">
          <p class="post-category">{{ formatCategory(post.category) }}</p>

          <h2>
            <RouterLink :to="`/posts/${post.id}`">
              {{ post.title }}
            </RouterLink>
          </h2>

          <p class="summary">
            {{ post.summary || "暂无摘要" }}
          </p>

          <p class="meta">
            {{ formatDate(post.created_at) }}
          </p>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getPosts } from "../api/posts";

const posts = ref([]);
const loading = ref(false);
const error = ref("");
const activeCategory = ref("");

async function loadPosts(category = "") {
  activeCategory.value = category;
  loading.value = true;
  error.value = "";

  try {
    const params = category ? { category } : {};
    const response = await getPosts(params);
    posts.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = "文章加载失败，请检查后端是否启动或 CORS 是否配置正确";
  } finally {
    loading.value = false;
  }
}

function formatCategory(category) {
  if (category === "life") return "生活记录";
  if (category === "study") return "学习笔记";
  return category || "未分类";
}

function formatDate(dateString) {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString();
}

onMounted(() => {
  loadPosts();
});
</script>

<style scoped>
.records-page {
  max-width: 1180px;
  margin: 0 auto;
  padding: 72px 24px;
}

.records-header {
  margin-bottom: 28px;
}

.eyebrow {
  margin: 0 0 12px;
  color: #b87b8b;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.records-header h1 {
  margin: 0;
  color: #151515;
  font-size: 44px;
  line-height: 1.1;
  letter-spacing: -1.2px;
}


.tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 30px 0;
}

.tabs button {
  padding: 9px 18px;
  border: 1px solid rgba(216, 154, 170, 0.28);
  border-radius: 999px;
  color: #8f5f6b;
  background: rgba(255, 255, 255, 0.58);
  transition:
    color 0.2s ease,
    background 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease;
}

.tabs button:hover,
.tabs button.active {
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

.post-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
}

.post-card {
  overflow: hidden;
  border: 1px solid rgba(90, 50, 64, 0.08);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 18px 48px rgba(90, 50, 64, 0.055);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.post-card:hover {
  transform: translateY(-4px);
  border-color: rgba(184, 123, 139, 0.24);
  box-shadow: 0 24px 64px rgba(90, 50, 64, 0.08);
}

.cover-link {
  display: block;
  text-decoration: none;
}

.cover-image,
.cover-placeholder {
  width: 100%;
  aspect-ratio: 16 / 10;
  display: block;
}

.cover-image {
  object-fit: cover;
}

.cover-placeholder {
  display: grid;
  place-items: center;
  color: #b87b8b;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  background:
    radial-gradient(circle at 20% 18%, rgba(255, 237, 242, 0.95), transparent 34%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 241, 245, 0.78));
}

.post-content {
  padding: 20px 20px 22px;
}

.post-category {
  margin: 0 0 10px;
  color: #b87b8b;
  font-size: 13px;
  font-weight: 700;
}

.post-card h2 {
  margin: 0;
  font-size: 22px;
  line-height: 1.35;
  letter-spacing: -0.4px;
}

.post-card h2 a {
  color: #202020;
  text-decoration: none;
}

.post-card h2 a:hover {
  color: #b87b8b;
}

.summary {
  display: -webkit-box;
  min-height: 58px;
  margin: 14px 0 0;
  overflow: hidden;
  color: #5d5558;
  line-height: 1.75;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.meta {
  margin: 16px 0 0;
  color: #8b7c82;
  font-size: 14px;
}

@media (max-width: 960px) {
  .post-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .records-page {
    padding: 42px 18px;
  }

  .records-header h1 {
    font-size: 36px;
  }

  .post-list {
    grid-template-columns: 1fr;
  }
}
</style>