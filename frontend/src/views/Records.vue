<template>
  <div class="page-shell records-page">
    <header class="page-heading">
      <p class="eyebrow">Journal & growth</p>
      <h1>沿途记录</h1>
      <p>生活被写成片段，学习被连成路径。每一次记录，都是成长树上的一点微光。</p>
    </header>

    <div class="pill-tabs">
      <button :class="{ active: activeView === 'all' }" @click="switchPosts('')">全部</button>
      <button :class="{ active: activeView === 'life' }" @click="switchPosts('life')">生活记录</button>
      <button :class="{ active: activeView === 'study' }" @click="switchPosts('study')">学习笔记</button>
      <button :class="{ active: activeView === 'learning' }" @click="activeView = 'learning'">成长树</button>
    </div>

    <section v-if="activeView === 'learning'" class="learning-tree">
      <div v-if="learningLoading" class="state-card">正在读取成长轨迹…</div>
      <div v-else-if="!learningNodes.length" class="state-card">成长树还没有节点。</div>
      <article v-for="(node, index) in learningNodes" :key="node.id" :class="['learning-node', node.status]">
        <div class="tree-line"><span>{{ node.status === 'completed' ? '✓' : node.status === 'active' ? '·' : index + 1 }}</span></div>
        <div class="node-copy surface">
          <div><small>{{ formatNodeStatus(node.status) }}</small><time>{{ formatDate(node.lit_at) || "等待点亮" }}</time></div>
          <h2>{{ node.title }}</h2>
          <p>{{ node.description || "这一段学习故事正在书写。" }}</p>
        </div>
      </article>
    </section>

    <section v-else>
      <div v-if="loading" class="state-card">正在翻阅记录…</div>
      <div v-else-if="error" class="state-card error">{{ error }}</div>
      <div v-else-if="!posts.length" class="state-card">这里暂时还是一页留白。</div>
      <div v-else class="post-grid">
        <article v-for="post in posts" :key="post.id" :class="['post-card', { pinned: post.is_pinned }]">
          <RouterLink class="post-cover" :to="`/posts/${post.id}`">
            <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" loading="lazy" />
            <div v-else class="cover-placeholder"><span>✦</span><small>Magnolia Nook</small></div>
            <span v-if="post.is_pinned" class="pin-label">置顶</span>
          </RouterLink>
          <div class="post-copy">
            <div class="post-meta"><span>{{ formatCategory(post.category) }}</span><time>{{ formatDate(post.published_at || post.created_at) }}</time></div>
            <h2><RouterLink :to="`/posts/${post.id}`">{{ post.title }}</RouterLink></h2>
            <p>{{ post.summary || "没有摘要，点进去看看吧。" }}</p>
            <div v-if="post.tags" class="tags"><span v-for="tag in splitTags(post.tags)" :key="tag"># {{ tag }}</span></div>
          </div>
        </article>
      </div>

      <div v-if="totalPages > 1" class="pagination">
        <button class="secondary-button" :disabled="currentPage <= 1" @click="changePage(currentPage - 1)">上一页</button>
        <span>{{ currentPage }} / {{ totalPages }}</span>
        <button class="secondary-button" :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)">下一页</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getPosts } from "../api/posts";
import { getLearningNodes } from "../api/content";

const activeView = ref("all");
const posts = ref([]); const loading = ref(false); const error = ref("");
const currentPage = ref(1); const totalPages = ref(1); const activeCategory = ref("");
const learningNodes = ref([]); const learningLoading = ref(false);

async function loadPosts(category = activeCategory.value, page = 1) {
  activeCategory.value = category; currentPage.value = page; loading.value = true; error.value = "";
  try {
    const params = { page, page_size: 9 }; if (category) params.category = category;
    const { data } = await getPosts(params); posts.value = data.items; totalPages.value = data.total_pages || 1;
  } catch { error.value = "记录加载失败，请稍后再试。"; }
  finally { loading.value = false; }
}
async function loadLearning() {
  learningLoading.value = true;
  try { learningNodes.value = (await getLearningNodes()).data; } catch { learningNodes.value = []; }
  finally { learningLoading.value = false; }
}
function switchPosts(category) { activeView.value = category || "all"; loadPosts(category, 1); }
function changePage(page) { if (page >= 1 && page <= totalPages.value) loadPosts(activeCategory.value, page); }
function formatCategory(value) { return value === "life" ? "生活记录" : "学习笔记"; }
function formatNodeStatus(value) { return ({ completed: "已经点亮", active: "正在进行", locked: "未来节点" })[value] || value; }
function formatDate(value) { return value ? new Date(value).toLocaleDateString("zh-CN", { year: "numeric", month: "short", day: "numeric" }) : ""; }
function splitTags(value) { return value.split(/[,，]/).map((tag) => tag.trim()).filter(Boolean); }
onMounted(() => { loadPosts(); loadLearning(); });
</script>

<style scoped>
.post-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; }
.post-card { position: relative; border: 1px solid var(--line); border-radius: 22px; background: rgba(255,253,249,.82); box-shadow: var(--shadow-sm); overflow: hidden; transition: .22s ease; }
.post-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-lg); }
.post-card.pinned { grid-column: span 2; display: grid; grid-template-columns: 1.08fr .92fr; }
.post-cover { position: relative; min-height: 230px; display: block; overflow: hidden; text-decoration: none; }
.post-cover img, .cover-placeholder { width: 100%; height: 100%; min-height: 230px; display: grid; place-items: center; object-fit: cover; transition: transform .4s ease; }
.post-card:hover img { transform: scale(1.035); }
.cover-placeholder { align-content: center; gap: 8px; color: var(--rose-600); background: linear-gradient(145deg, var(--rose-50), #f2f0e9); }
.cover-placeholder span { font-size: 42px; }.cover-placeholder small { letter-spacing: .14em; }
.pin-label { position: absolute; left: 14px; top: 14px; padding: 5px 10px; border-radius: 999px; color: #fff; background: rgba(120,64,78,.85); font-size: 11px; }
.post-copy { padding: 23px; }
.post-meta { display: flex; justify-content: space-between; gap: 12px; color: var(--muted); font-size: 11px; letter-spacing: .08em; }
.post-meta span { color: var(--rose-600); font-weight: 750; }
.post-copy h2 { margin: 15px 0 12px; font: 500 24px/1.4 Georgia, "Songti SC", serif; }
.post-copy h2 a { text-decoration: none; }.post-copy p { margin: 0; color: var(--muted-strong); line-height: 1.75; }
.tags { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px; color: var(--rose-600); font-size: 11px; }
.pagination { display: flex; justify-content: center; align-items: center; gap: 18px; margin-top: 38px; color: var(--muted); }
.learning-tree { max-width: 900px; margin: 20px auto 0; }
.learning-node { display: grid; grid-template-columns: 72px 1fr; gap: 18px; min-height: 180px; }
.tree-line { position: relative; display: flex; justify-content: center; }
.tree-line::after { content: ""; position: absolute; top: 44px; bottom: -2px; width: 1px; background: var(--rose-200); }
.learning-node:last-child .tree-line::after { display: none; }
.tree-line span { z-index: 1; width: 42px; height: 42px; display: grid; place-items: center; border: 1px solid var(--rose-200); border-radius: 50%; color: var(--muted); background: var(--paper); }
.learning-node.completed .tree-line span, .learning-node.active .tree-line span { color: #fff; border-color: var(--rose-600); background: var(--rose-600); box-shadow: 0 0 0 7px var(--rose-50); }
.learning-node.active .tree-line span { animation: pulse 1.7s ease infinite; }
@keyframes pulse { 50% { box-shadow: 0 0 0 12px rgba(247,225,229,.2); } }
.node-copy { margin-bottom: 28px; padding: 24px 28px; }
.node-copy > div { display: flex; justify-content: space-between; color: var(--muted); font-size: 11px; }.node-copy small { color: var(--rose-600); font-weight: 750; }
.node-copy h2 { margin: 13px 0 8px; font: 500 24px Georgia, "Songti SC", serif; }.node-copy p { margin: 0; color: var(--muted-strong); line-height: 1.8; }
.learning-node.locked { opacity: .56; }
@media (max-width: 900px) { .post-grid { grid-template-columns: repeat(2, 1fr); }.post-card.pinned { grid-column: span 2; } }
@media (max-width: 620px) { .post-grid { grid-template-columns: 1fr; }.post-card.pinned { grid-column: auto; display: block; }.learning-node { grid-template-columns: 46px 1fr; gap: 8px; } }
</style>
