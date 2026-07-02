<template>
  <div class="search-page">
    <!-- 页面标题区域 -->
    <header class="search-header">
      <p class="eyebrow">Search</p>
      <h1>搜索</h1>
      <p class="search-subtitle">
        输入标题，摘要，正文中的关键词查找文章。
      </p>
    </header>

    <!-- 搜索输入区域 -->
    <div class="search-box">
      <input
        v-model="keyword"
        type="text"
        placeholder="输入关键词搜索文章"
        @keyup.enter="handleSearch"
      />
      <button @click="handleSearch">搜索</button>
    </div>

    <!-- 状态提示 -->
    <div v-if="loading" class="state-card">搜索中...</div>
    <div v-else-if="error" class="state-card error">{{ error }}</div>
    <div v-else-if="!searched" class="state-card">
      请输入关键词开始搜索
    </div>
    <div v-else-if="results.length === 0" class="state-card">
      没有找到相关文章
    </div>

    <!-- 搜索结果 -->
    <div v-else class="result-list">
      <article v-for="post in results" :key="post.id" class="result-card">
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

        <div class="result-content">
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
import { ref } from "vue";
import { searchPosts } from "../api/posts";

const keyword = ref("");
const results = ref([]);
const loading = ref(false);
const error = ref("");
const searched = ref(false);

async function handleSearch() {
  const q = keyword.value.trim();

  if (!q) {
    error.value = "请输入搜索关键词";
    results.value = [];
    searched.value = false;
    return;
  }

  loading.value = true;
  error.value = "";
  searched.value = true;

  try {
    const response = await searchPosts(q);
    results.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = "搜索失败，请检查后端接口是否正常";
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
</script>

<style scoped>
.search-page {
  max-width: 1180px;
  margin: 0 auto;
  padding: 72px 24px;
}

.search-header {
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

.search-header h1 {
  margin: 0;
  color: #151515;
  font-size: 44px;
  line-height: 1.1;
  letter-spacing: -1.2px;
}

.search-subtitle {
  max-width: 640px;
  margin: 18px 0 0;
  color: #6f6065;
  font-size: 17px;
  line-height: 1.9;
}

.search-box {
  display: flex;
  gap: 12px;
  margin: 30px 0;
  padding: 10px;
  border: 1px solid rgba(90, 50, 64, 0.08);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 18px 48px rgba(90, 50, 64, 0.045);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.search-box input {
  flex: 1;
  min-width: 0;
  padding: 0 14px;
  border: none;
  outline: none;
  color: #1f1f1f;
  background: transparent;
}

.search-box input::placeholder {
  color: #9c8f94;
}

.search-box button {
  padding: 10px 22px;
  border: 1px solid #b87b8b;
  border-radius: 999px;
  color: #ffffff;
  background: #b87b8b;
  transition:
    background-color 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease;
}

.search-box button:hover {
  border-color: #9f6473;
  background: #9f6473;
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

.result-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
}

.result-card {
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

.result-card:hover {
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

.result-content {
  padding: 20px 20px 22px;
}

.post-category {
  margin: 0 0 10px;
  color: #b87b8b;
  font-size: 13px;
  font-weight: 700;
}

.result-card h2 {
  margin: 0;
  font-size: 22px;
  line-height: 1.35;
  letter-spacing: -0.4px;
}

.result-card h2 a {
  color: #202020;
  text-decoration: none;
}

.result-card h2 a:hover {
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
  .result-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .search-page {
    padding: 42px 18px;
  }

  .search-header h1 {
    font-size: 36px;
  }

  .search-box {
    border-radius: 24px;
    flex-direction: column;
  }

  .search-box input {
    min-height: 42px;
  }

  .result-list {
    grid-template-columns: 1fr;
  }
}
</style>